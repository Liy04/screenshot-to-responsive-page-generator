import copy
import re
import time
from pathlib import Path
from typing import Any

try:
    from .layout_quality_repair import normalize_intermediate_sections_for_quality
    from .layout_static_generator import compile_preview_document
    from .image_layout_resolver import infer_template_key_from_image_name, resolve_fallback_image_layout
    from .layout_validator import ValidationMessage, validate_layout_document
    from .real_ai_layout_client import PROMPT_VERSION, RealAIError, get_configured_model, request_layout_intermediate
except ImportError:
    from layout_quality_repair import normalize_intermediate_sections_for_quality
    from layout_static_generator import compile_preview_document
    from image_layout_resolver import infer_template_key_from_image_name, resolve_fallback_image_layout
    from layout_validator import ValidationMessage, validate_layout_document
    from real_ai_layout_client import PROMPT_VERSION, RealAIError, get_configured_model, request_layout_intermediate


ALLOWED_IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg", ".webp"}
MAX_IMAGE_SIZE_BYTES = 5 * 1024 * 1024
FALLBACK_REASON_MODEL_UNAVAILABLE = "MODEL_UNAVAILABLE"
FALLBACK_REASON_MODEL_NON_JSON_OUTPUT = "MODEL_NON_JSON_OUTPUT"
FALLBACK_REASON_JSON_PARSE_FAILED = "JSON_PARSE_FAILED"
FALLBACK_REASON_SCHEMA_VALIDATION_FAILED = "SCHEMA_VALIDATION_FAILED"
FALLBACK_REASON_IMAGE_READ_FAILED = "IMAGE_READ_FAILED"
FALLBACK_REASON_WORKER_TIMEOUT = "WORKER_TIMEOUT"
FALLBACK_REASON_PREVIEW_COMPILE_FAILED = "PREVIEW_COMPILE_FAILED"

STYLE_KEY_WHITELIST = {
    "backgroundColor",
    "color",
    "fontSize",
    "fontWeight",
    "textAlign",
    "padding",
    "margin",
    "gap",
    "borderRadius",
    "boxShadow",
    "border",
    "width",
    "height",
    "display",
    "flexDirection",
    "alignItems",
    "justifyContent",
    "objectFit",
}

UNSAFE_STYLE_VALUE_FRAGMENTS = {
    "javascript:",
    "expression(",
    "url(",
    "<script",
    "onerror=",
    "onclick=",
    "data:text/html",
    "@import",
    "position: fixed",
    "position: absolute",
}

DEFAULT_NODE_STYLES: dict[str, dict[str, Any]] = {
    "page": {
        "backgroundColor": "#ffffff",
        "color": "#111827",
        "fontSize": "16px",
    },
    "section": {
        "padding": "32px",
        "gap": "16px",
    },
    "card": {
        "backgroundColor": "#ffffff",
        "border": "1px solid #d1d5db",
        "borderRadius": "12px",
        "padding": "20px",
        "boxShadow": "0 8px 24px rgba(15, 23, 42, 0.08)",
    },
    "button": {
        "backgroundColor": "#2563eb",
        "color": "#ffffff",
        "borderRadius": "8px",
        "padding": "10px 16px",
        "fontWeight": "700",
        "textAlign": "center",
    },
    "input": {
        "backgroundColor": "#ffffff",
        "border": "1px solid #d1d5db",
        "borderRadius": "8px",
        "padding": "10px 12px",
    },
    "form": {
        "gap": "12px",
        "padding": "20px",
    },
    "text": {
        "color": "#111827",
        "fontSize": "16px",
    },
}

ALLOWED_LAYOUT_NODE_TYPES = {
    "page",
    "section",
    "container",
    "text",
    "button",
    "image",
    "card",
    "list",
    "listItem",
    "form",
    "input",
}


def message_to_dict(message: ValidationMessage) -> dict[str, str]:
    return {
        "code": message.code,
        "message": message.message,
        "path": message.path,
    }


def make_message(code: str, message: str, path: str = "$") -> ValidationMessage:
    return ValidationMessage(code=code, message=message, path=path)


def make_result(
    job_id: str,
    status: str,
    mode: str,
    fallback_used: bool,
    source_type: str,
    layout_json: dict[str, Any] | None,
    errors: list[ValidationMessage],
    warnings: list[ValidationMessage],
    message: str,
    preview_html: str = "",
    prompt_version: str | None = PROMPT_VERSION,
    fallback_reason: str | None = None,
) -> dict[str, Any]:
    return {
        "jobId": job_id,
        "status": status,
        "mode": mode,
        "fallbackUsed": fallback_used,
        "fallbackReason": fallback_reason,
        "sourceType": source_type,
        "promptVersion": prompt_version,
        "layoutJson": layout_json,
        "previewHtml": preview_html,
        "validation": {
            "ok": not errors,
            "errors": [message_to_dict(error) for error in errors],
            "warnings": [message_to_dict(warning) for warning in warnings],
        },
        "message": message,
    }


def result_model_for_mode(mode: str) -> str | None:
    if mode == "fallback-only":
        return None
    return get_configured_model()


def add_runtime_metadata(
    result: dict[str, Any],
    started_at: float,
    model: str | None,
) -> dict[str, Any]:
    result["durationMs"] = int((time.perf_counter() - started_at) * 1000)
    result["model"] = model
    return result


def validate_image_path(image_path: str | Path) -> tuple[Path | None, list[ValidationMessage]]:
    path = Path(image_path)
    errors: list[ValidationMessage] = []

    if not path.exists():
        errors.append(make_message("IMAGE_PATH_NOT_FOUND", "Image path does not exist", "$.imagePath"))
        return None, errors

    if not path.is_file():
        errors.append(make_message("IMAGE_PATH_INVALID", "Image path must point to a file", "$.imagePath"))
        return None, errors

    if path.suffix.lower() not in ALLOWED_IMAGE_SUFFIXES:
        errors.append(
            make_message(
                "IMAGE_TYPE_UNSUPPORTED",
                "Only png, jpg, jpeg and webp are supported",
                "$.imagePath",
            )
        )
        return None, errors

    if path.stat().st_size > MAX_IMAGE_SIZE_BYTES:
        errors.append(
            make_message(
                "IMAGE_SIZE_EXCEEDED",
                "Image file must be 5MB or smaller",
                "$.imagePath",
            )
        )
        return None, errors

    return path, errors


def normalize_page_type(value: Any) -> str:
    if not isinstance(value, str) or not value.strip():
        return "generic"
    return value.strip().lower()


def default_page_name(image_name: str) -> str:
    return Path(image_name).stem.replace("-", " ").replace("_", " ").title() or "Generated Page"


def default_bounds(x: int, y: int, width: int, height: int) -> dict[str, int]:
    return {
        "x": x,
        "y": y,
        "width": width,
        "height": height,
    }


def default_constraints(horizontal: str = "fill", vertical: str = "hug") -> dict[str, str]:
    return {
        "horizontal": horizontal,
        "vertical": vertical,
    }


def make_layout_warning(target: str, message: str) -> dict[str, str]:
    return {
        "target": target,
        "message": message,
    }


def is_safe_style_value(value: Any) -> bool:
    if isinstance(value, (int, float)):
        return True
    if not isinstance(value, str):
        return False
    lowered = value.strip().lower()
    if not lowered:
        return False
    return not any(fragment in lowered for fragment in UNSAFE_STYLE_VALUE_FRAGMENTS)


def sanitize_style(style: Any, target: str, warnings: list[dict[str, str]]) -> dict[str, Any]:
    if not isinstance(style, dict):
        return {}

    sanitized: dict[str, Any] = {}
    for key, value in style.items():
        if key not in STYLE_KEY_WHITELIST:
            warnings.append(
                make_layout_warning(
                    target,
                    f"Unsupported style key was ignored: {key}",
                )
            )
            continue
        if not is_safe_style_value(value):
            warnings.append(
                make_layout_warning(
                    target,
                    f"Unsafe style value was ignored: {key}",
                )
            )
            continue
        sanitized[key] = value
    return sanitized


def default_style_for_node(node_type: str, role: str) -> dict[str, Any]:
    style = copy.deepcopy(DEFAULT_NODE_STYLES.get(node_type, {}))
    normalized_role = role.lower()
    if node_type == "text" and normalized_role in {"heading", "title"}:
        style.update({"fontSize": "28px", "fontWeight": "700"})
    if node_type == "text" and normalized_role == "metric":
        style.update({"fontSize": "32px", "fontWeight": "700"})
    if node_type == "text" and normalized_role == "label":
        style.update({"fontSize": "14px", "color": "#64748b", "fontWeight": "600"})
    if node_type == "card" and normalized_role == "metric":
        style.update({"display": "flex", "flexDirection": "column", "gap": "8px", "width": "220px"})
    if node_type == "section" and normalized_role in {"hero", "header", "dashboard", "cards", "form"}:
        style.update(copy.deepcopy(DEFAULT_NODE_STYLES.get("form" if normalized_role == "form" else "section", {})))
    if node_type == "section" and normalized_role in {"metrics", "dashboard"}:
        style.update({"display": "flex", "flexDirection": "row", "gap": "16px"})
    if node_type == "form":
        style.update({"display": "flex", "flexDirection": "column", "gap": "12px"})
    return style


def merge_default_and_sanitized_style(
    node_type: str,
    role: str,
    provided_style: Any,
    target: str,
    warnings: list[dict[str, str]],
) -> dict[str, Any]:
    style = default_style_for_node(node_type, role)
    style.update(sanitize_style(provided_style, target, warnings))
    return style


def infer_children_from_section(
    section: dict[str, Any],
    start_y: int,
    assets: list[dict[str, Any]],
    warnings: list[dict[str, str]],
) -> list[dict[str, Any]]:
    elements = section.get("elements")
    if not isinstance(elements, list):
        elements = []
    return infer_children_from_elements(elements, start_y, assets, warnings, f"ai-section-{start_y}")


def infer_children_from_elements(
    elements: list[Any],
    start_y: int,
    assets: list[dict[str, Any]],
    warnings: list[dict[str, str]],
    id_prefix: str,
) -> list[dict[str, Any]]:
    children: list[dict[str, Any]] = []
    cursor_y = start_y
    for index, element in enumerate(elements):
        if isinstance(element, str):
            element = {"type": "text", "role": "body", "content": element}
        if not isinstance(element, dict):
            continue
        node_type = str(element.get("type", "text")).strip()
        node_type_lower = node_type.lower() if node_type else "text"
        if node_type_lower == "listitem":
            node_type_lower = "listItem"
        role = str(element.get("role", "content"))
        node_id = f"{id_prefix}-node-{index}"
        node: dict[str, Any] = {
            "id": node_id,
            "type": node_type_lower if node_type_lower in ALLOWED_LAYOUT_NODE_TYPES else "text",
            "role": role,
            "bounds": default_bounds(120, cursor_y, 440, 48),
            "style": {},
            "constraints": default_constraints(),
            "interactions": [],
            "children": [],
        }
        node["style"] = merge_default_and_sanitized_style(
            node["type"],
            role,
            element.get("style"),
            node_id,
            warnings,
        )

        if node["type"] in {"text", "button"}:
            content = element.get("content")
            node["content"] = content if isinstance(content, str) and content.strip() else f"{role} {index + 1}"
        elif node["type"] == "image":
            asset_id = f"{node_id}-asset"
            node["assetId"] = asset_id
            node["src"] = None
            node["bounds"] = default_bounds(120, cursor_y, 480, 240)
            assets.append(
                {
                    "id": asset_id,
                    "type": "image",
                    "status": "placeholder",
                }
            )
        elif node["type"] == "input":
            node["bounds"] = default_bounds(120, cursor_y, 360, 44)
            content = element.get("content")
            if not isinstance(content, str) or not content.strip():
                label = element.get("label")
                if isinstance(label, str) and label.strip():
                    content = label.strip()
            if isinstance(content, str) and content.strip():
                node["content"] = content.strip()
        elif node["type"] == "form":
            node["bounds"] = default_bounds(120, cursor_y, 560, 220)

        nested_elements = element.get("elements")
        if not isinstance(nested_elements, list):
            nested_elements = element.get("children")
        if isinstance(nested_elements, list) and node["type"] in {"container", "card", "list", "listItem", "form"}:
            node["children"] = infer_children_from_elements(
                nested_elements,
                cursor_y + 32,
                assets,
                warnings,
                node_id,
            )

        children.append(node)
        cursor_y += 72 if node["type"] != "image" else 264

    if not children:
        children.append(
            {
                "id": f"ai-section-{start_y}-title",
                "type": "text",
                "role": "heading",
                "content": "Generated layout from image",
                "bounds": default_bounds(120, start_y, 480, 48),
                "style": default_style_for_node("text", "heading"),
                "constraints": default_constraints(),
                "interactions": [],
                "children": [],
            }
        )

    return children


def flatten_intermediate_sections(sections: Any) -> list[dict[str, Any]]:
    if not isinstance(sections, list):
        return []

    flattened: list[dict[str, Any]] = []
    for section in sections:
        if not isinstance(section, dict):
            continue
        flattened.append(section)
        nested_sections = section.get("sections")
        if isinstance(nested_sections, list):
            flattened.extend(flatten_intermediate_sections(nested_sections))
    return flattened


def component_to_element(component: Any) -> dict[str, Any] | None:
    if isinstance(component, str):
        text = component.strip()
        if not text:
            return None
        return {"type": "text", "role": "body", "content": text}
    if not isinstance(component, dict):
        return None

    node_type = str(component.get("type", "text")).strip()
    node_type_lower = node_type.lower() if node_type else "text"
    role = str(component.get("role", "body")).strip() or "body"
    content = component.get("content")
    if not isinstance(content, str) or not content.strip():
        content = component.get("text")
    if not isinstance(content, str) or not content.strip():
        content = component.get("label")

    if node_type_lower in {"form", "container", "list", "listitem"}:
        nested_items = component.get("items")
        if not isinstance(nested_items, list):
            nested_items = component.get("elements")
        if not isinstance(nested_items, list):
            nested_items = component.get("children")

        nested_children: list[dict[str, Any]] = []
        if isinstance(nested_items, list):
            for item in nested_items:
                nested_element = component_to_element(item)
                if nested_element is not None:
                    nested_children.append(nested_element)
        if isinstance(content, str) and content.strip():
            nested_children.insert(0, {"type": "text", "role": "body", "content": content.strip()})

        normalized_type = "listItem" if node_type_lower == "listitem" else node_type_lower
        if nested_children:
            return {"type": normalized_type, "role": role, "elements": nested_children}
        if normalized_type == "form":
            return {"type": "form", "role": role, "elements": []}
        return None

    if node_type_lower == "card":
        card_children: list[dict[str, Any]] = []
        if isinstance(content, str) and content.strip():
            card_children.append(
                {
                    "type": "text",
                    "role": "heading" if role in {"card", "metric"} else "body",
                    "content": content.strip(),
                }
            )
        nested_items = component.get("items")
        if isinstance(nested_items, list):
            for item in nested_items[:4]:
                nested_element = component_to_element(item)
                if nested_element is not None:
                    card_children.append(nested_element)
        return {"type": "card", "role": role, "elements": card_children}

    if node_type_lower in {"button", "input", "image", "text"}:
        element: dict[str, Any] = {"type": node_type_lower, "role": role}
        if isinstance(content, str) and content.strip():
            element["content"] = content.strip()
        return element

    if node_type_lower == "listitem":
        element = {"type": "listItem", "role": role}
        if isinstance(content, str) and content.strip():
            element["content"] = content.strip()
        return element

    if isinstance(content, str) and content.strip():
        return {"type": "text", "role": role, "content": content.strip()}
    return None


def visual_inventory_regions_to_sections(regions: Any) -> list[dict[str, Any]]:
    if not isinstance(regions, list):
        return []

    sections: list[dict[str, Any]] = []
    for region in regions:
        if not isinstance(region, dict):
            continue
        role = str(region.get("role", "content"))
        elements: list[dict[str, Any]] = []
        seen_texts: set[str] = set()
        region_texts = [text.strip() for text in region.get("texts", []) if isinstance(text, str) and text.strip()]

        if role in {"metrics", "dashboard"} and len(region_texts) >= 2:
            for pair_index in range(0, len(region_texts), 2):
                label = region_texts[pair_index]
                value = region_texts[pair_index + 1] if pair_index + 1 < len(region_texts) else ""
                card_children = [{"type": "text", "role": "label", "content": label}]
                if value:
                    card_children.append({"type": "text", "role": "metric", "content": value})
                elements.append({"type": "card", "role": "metric", "elements": card_children})
                seen_texts.add(label.lower())
                if value:
                    seen_texts.add(value.lower())
        for text in region_texts:
            normalized = text
            if normalized.lower() in seen_texts:
                continue
            seen_texts.add(normalized.lower())
            text_role = "heading" if not elements and role in {"hero", "header", "content"} else "body"
            elements.append({"type": "text", "role": text_role, "content": normalized})

        components = region.get("components")
        if not isinstance(components, list):
            components = region.get("elements")
        if isinstance(components, list):
            for component in components:
                element = component_to_element(component)
                if element is None:
                    continue
                content = element.get("content")
                if isinstance(content, str) and content.strip().lower() in seen_texts:
                    continue
                elements.append(element)

        if elements:
            sections.append({"role": role, "elements": elements})
    return sections


def top_level_texts_to_sections(texts: Any) -> list[dict[str, Any]]:
    if not isinstance(texts, list):
        return []
    elements = []
    for index, text in enumerate(texts):
        if not isinstance(text, str) or not text.strip():
            continue
        elements.append(
            {
                "type": "text",
                "role": "heading" if index == 0 else "body",
                "content": text.strip(),
            }
        )
    if not elements:
        return []
    return [{"role": "content", "elements": elements}]


def map_intermediate_to_layout_json(intermediate: dict[str, Any], image_name: str) -> dict[str, Any]:
    page_name = intermediate.get("pageName")
    if not isinstance(page_name, str) or not page_name.strip():
        page_name = default_page_name(image_name)

    page_type = normalize_page_type(intermediate.get("pageType"))
    sections = flatten_intermediate_sections(intermediate.get("sections"))
    if not sections:
        sections = visual_inventory_regions_to_sections(intermediate.get("regions"))
    if not sections:
        sections = top_level_texts_to_sections(intermediate.get("texts"))

    assets: list[dict[str, Any]] = []
    layout_sections: list[dict[str, Any]] = []
    layout_warnings: list[dict[str, str]] = []
    section_y = 80

    if not sections:
        sections = [{"role": "content", "elements": [{"type": "text", "role": "heading", "content": page_name}]}]

    for index, section in enumerate(sections):
        if not isinstance(section, dict):
            continue
        role = str(section.get("role", f"section{index + 1}"))
        section_id = f"ai-section-{index + 1}"
        children = infer_children_from_section(section, section_y + 32, assets, layout_warnings)
        section_height = max(220, 72 * max(len(children), 1) + 64)
        layout_sections.append(
            {
                "id": section_id,
                "type": "section",
                "role": role,
                "bounds": default_bounds(80, section_y, 1280, section_height),
                "style": merge_default_and_sanitized_style(
                    "section",
                    role,
                    section.get("style"),
                    section_id,
                    layout_warnings,
                ),
                "constraints": default_constraints(),
                "interactions": [],
                "children": children,
            }
        )
        section_y += section_height + 32

    return {
        "version": "0.1",
        "page": {
            "name": page_name,
            "type": page_type,
            "viewport": {
                "width": 1440,
                "height": max(900, section_y + 80),
            },
        },
        "source": {
            "type": "screenshot",
            "fileUrl": None,
            "figmaFileKey": None,
            "figmaNodeId": None,
        },
        "tokens": {
            "colors": {},
            "typography": {},
            "spacing": {},
            "radius": {},
        },
        "layout": {
            "id": "ai-root",
            "type": "page",
            "role": "page",
            "bounds": default_bounds(0, 0, 1440, max(900, section_y + 80)),
            "style": default_style_for_node("page", "page"),
            "constraints": default_constraints("fill", "fill"),
            "interactions": [],
            "children": layout_sections,
        },
        "assets": assets,
        "responsive": {
            "breakpoints": {
                "mobile": 390,
                "tablet": 768,
                "desktop": 1440,
            },
            "rules": [],
        },
        "assumptions": [
            {
                "target": "ai-root",
                "message": "AI output was mapped into the Layout JSON v0.1 structure.",
            }
        ],
        "warnings": layout_warnings,
    }


def normalize_text_list(values: Any) -> list[str]:
    if not isinstance(values, list):
        return []
    normalized: list[str] = []
    seen: set[str] = set()
    for value in values:
        if not isinstance(value, str):
            continue
        text = value.strip()
        if not text:
            continue
        key = text.lower()
        if key in seen:
            continue
        seen.add(key)
        normalized.append(text)
    return normalized


def normalize_region_components(values: Any) -> list[dict[str, Any]]:
    if not isinstance(values, list):
        return []
    normalized: list[dict[str, Any]] = []
    for item in values:
        if isinstance(item, str):
            content = item.strip()
            if not content:
                continue
            normalized.append({"type": "text", "role": "body", "content": content})
            continue
        if not isinstance(item, dict):
            continue

        element_type = str(item.get("type", "text")).strip() or "text"
        element_type_lower = element_type.lower()
        if element_type_lower == "listitem":
            element_type = "listItem"
            element_type_lower = "listitem"
        elif element_type_lower in {"form", "container", "list", "card", "input", "button", "image", "text"}:
            element_type = element_type_lower
        role = str(item.get("role", "body")).strip() or "body"
        component: dict[str, Any] = {"type": element_type, "role": role}

        content = None
        for key in ("content", "text", "label"):
            value = item.get(key)
            if isinstance(value, str) and value.strip():
                content = value.strip()
                break
        if content is not None:
            component["content"] = content

        if element_type == "card":
            items = item.get("items")
            if isinstance(items, list):
                normalized_items: list[Any] = []
                for value in items:
                    if isinstance(value, str):
                        stripped = value.strip()
                        if stripped:
                            normalized_items.append(stripped)
                    elif isinstance(value, dict):
                        normalized_items.append(copy.deepcopy(value))
                if normalized_items:
                    component["items"] = normalized_items
            if "content" not in component and "items" not in component:
                continue
            normalized.append(component)
            continue

        if element_type in {"form", "container", "list", "listItem"}:
            items = item.get("items")
            if not isinstance(items, list):
                items = item.get("elements")
            if not isinstance(items, list):
                items = item.get("children")
            if isinstance(items, list):
                normalized_items = []
                for value in items:
                    if isinstance(value, str):
                        stripped = value.strip()
                        if stripped:
                            normalized_items.append(stripped)
                    elif isinstance(value, dict):
                        normalized_items.append(copy.deepcopy(value))
                if normalized_items:
                    component["items"] = normalized_items
            if "content" not in component and "items" not in component and element_type != "form":
                continue
            normalized.append(component)
            continue

        if element_type in {"text", "button", "input", "listItem"} and "content" not in component:
            continue
        normalized.append(component)
    return normalized


def normalize_visual_inventory_regions(values: Any) -> list[dict[str, Any]]:
    if not isinstance(values, list):
        return []
    normalized_regions: list[dict[str, Any]] = []
    for region in values:
        if not isinstance(region, dict):
            continue
        role = region.get("role")
        if isinstance(role, str) and role.strip():
            normalized_role = role.strip().lower()
        else:
            normalized_role = "content"
        texts = normalize_text_list(region.get("texts"))
        components = normalize_region_components(region.get("components"))
        if texts or components:
            normalized_regions.append(
                {
                    "role": normalized_role,
                    "texts": texts,
                    "components": components,
                }
            )
    return normalized_regions


def repair_intermediate_payload(intermediate: Any, image_name: str) -> tuple[dict[str, Any], bool]:
    if not isinstance(intermediate, dict):
        return {}, False

    repaired = copy.deepcopy(intermediate)
    used = False

    page_name = repaired.get("pageName")
    normalized_page_name = page_name.strip() if isinstance(page_name, str) else ""
    if not normalized_page_name:
        normalized_page_name = default_page_name(image_name)
    if normalized_page_name != page_name:
        used = True
    repaired["pageName"] = normalized_page_name

    page_type = repaired.get("pageType")
    normalized_page_type = normalize_page_type(page_type)
    if normalized_page_type != page_type:
        used = True
    repaired["pageType"] = normalized_page_type

    normalized_texts = normalize_text_list(repaired.get("texts"))
    if normalized_texts != repaired.get("texts"):
        used = True
    repaired["texts"] = normalized_texts

    normalized_regions = normalize_visual_inventory_regions(repaired.get("regions"))
    if normalized_regions != repaired.get("regions"):
        used = True
    repaired["regions"] = normalized_regions

    sections = repaired.get("sections")
    if not isinstance(sections, list):
        inventory_sections = visual_inventory_regions_to_sections(repaired.get("regions"))
        if not inventory_sections:
            inventory_sections = top_level_texts_to_sections(repaired.get("texts"))
        if inventory_sections:
            repaired["sections"] = inventory_sections
            sections = repaired["sections"]
            used = True

    if not isinstance(sections, list):
        repaired["sections"] = []
        sections = repaired["sections"]
        used = True

    normalized_sections, sections_changed = normalize_intermediate_sections_for_quality(sections)
    if sections_changed:
        repaired["sections"] = normalized_sections
        used = True

    stable_payload: dict[str, Any] = {
        "pageName": repaired["pageName"],
        "pageType": repaired["pageType"],
        "texts": repaired["texts"],
        "regions": repaired["regions"],
        "sections": repaired["sections"],
    }
    if stable_payload != intermediate:
        used = True
    return stable_payload, used


def repair_layout_json(document: Any, image_name: str) -> dict[str, Any]:
    if not isinstance(document, dict):
        document = {}

    repaired = copy.deepcopy(document)
    repaired.setdefault("version", "0.1")
    repaired.setdefault(
        "page",
        {
            "name": Path(image_name).stem or "Generated Page",
            "type": "generic",
            "viewport": {"width": 1440, "height": 900},
        },
    )
    repaired.setdefault(
        "source",
        {
            "type": "screenshot",
            "fileUrl": None,
            "figmaFileKey": None,
            "figmaNodeId": None,
        },
    )
    repaired.setdefault("tokens", {"colors": {}, "typography": {}, "spacing": {}, "radius": {}})
    repaired.setdefault("assets", [])
    repaired.setdefault(
        "responsive",
        {
            "breakpoints": {"mobile": 390, "tablet": 768, "desktop": 1440},
            "rules": [],
        },
    )
    repaired.setdefault("assumptions", [])
    repaired.setdefault("warnings", [])

    layout = repaired.get("layout")
    if not isinstance(layout, dict):
        repaired["layout"] = {}

    def infer_node_type(raw_type: Any, node: dict[str, Any], is_root: bool, *, parent_type: str = "") -> str:
        normalized = str(raw_type).strip()
        normalized_lower = normalized.lower() if normalized else ""
        if normalized_lower == "listitem":
            return "listItem"
        if normalized_lower in ALLOWED_LAYOUT_NODE_TYPES:
            return normalized_lower
        label = node.get("label")
        if isinstance(label, str) and label.strip():
            return "input"
        role = str(node.get("role", "")).strip().lower()
        if role in {"primary-action", "button", "cta", "submit", "nav"} or "button" in role or "action" in role:
            return "button"
        if is_root:
            return "page"
        content = node.get("content")
        if isinstance(content, str) and content.strip():
            node_id = str(node.get("id", "")).lower()
            if parent_type == "form" and (
                "button" in node_id or "action" in node_id or "submit" in node_id or role in {"primary-action", "submit"}
            ):
                return "button"
            return "text"
        if isinstance(node.get("children"), list) and node.get("children"):
            return "container"
        return "text"

    def make_stable_repaired_node_id(node_type: str, path: str) -> str:
        path_slug = re.sub(r"[^a-zA-Z0-9]+", "-", path).strip("-").lower()
        if not path_slug:
            path_slug = "root"
        return f"repaired-{node_type}-{path_slug}"

    def repair_node(
        node: Any,
        path: str,
        layout_warnings: list[dict[str, str]],
        *,
        is_root: bool = False,
        parent_type: str = "",
    ) -> dict[str, Any]:
        if not isinstance(node, dict):
            node = {}

        repaired_node = copy.deepcopy(node)
        node_type = infer_node_type(repaired_node.get("type"), repaired_node, is_root, parent_type=parent_type)
        repaired_node["type"] = node_type

        role = repaired_node.get("role")
        if not isinstance(role, str) or not role.strip():
            if node_type == "page":
                repaired_node["role"] = "page"
            elif node_type == "input":
                repaired_node["role"] = "text"
            elif node_type == "button":
                repaired_node["role"] = "primary-action"
            elif node_type == "text":
                repaired_node["role"] = "body"
            else:
                repaired_node["role"] = node_type
        else:
            repaired_node["role"] = role.strip()

        node_id = repaired_node.get("id")
        if not isinstance(node_id, str) or not node_id.strip():
            repaired_node["id"] = make_stable_repaired_node_id(node_type, path)

        repaired_node["style"] = merge_default_and_sanitized_style(
            node_type,
            repaired_node["role"],
            repaired_node.get("style"),
            repaired_node["id"],
            layout_warnings,
        )

        if node_type == "page":
            repaired_node.setdefault("bounds", default_bounds(0, 0, 1440, 900))
            repaired_node["constraints"] = default_constraints("fill", "fill")
        elif node_type == "section":
            repaired_node.setdefault("bounds", default_bounds(80, 80, 1280, 220))
            repaired_node["constraints"] = default_constraints("fill", "hug")
        elif node_type == "form":
            repaired_node.setdefault("bounds", default_bounds(120, 120, 560, 220))
            repaired_node["constraints"] = default_constraints("fill", "hug")
        elif node_type == "input":
            repaired_node.setdefault("bounds", default_bounds(120, 120, 360, 44))
            repaired_node["constraints"] = default_constraints("fill", "hug")
            content = repaired_node.get("content")
            if not isinstance(content, str) or not content.strip():
                label = repaired_node.get("label")
                if isinstance(label, str) and label.strip():
                    repaired_node["content"] = label.strip()
        elif node_type == "button":
            repaired_node.setdefault("bounds", default_bounds(120, 120, 200, 48))
            repaired_node["constraints"] = default_constraints("hug", "hug")
        elif node_type == "text":
            repaired_node.setdefault("bounds", default_bounds(120, 120, 440, 48))
            repaired_node["constraints"] = default_constraints("fill", "hug")
            content = repaired_node.get("content")
            if not isinstance(content, str) or not content.strip():
                repaired_node["content"] = "Text"
        else:
            repaired_node.setdefault("bounds", default_bounds(120, 120, 440, 120))
            repaired_node["constraints"] = default_constraints("fill", "hug")

        interactions = repaired_node.get("interactions")
        repaired_node["interactions"] = interactions if isinstance(interactions, list) else []

        children = repaired_node.get("children")
        if not isinstance(children, list):
            children = []
        repaired_children: list[dict[str, Any]] = []
        for index, child in enumerate(children):
            repaired_children.append(
                repair_node(
                    child,
                    f"{path}.children[{index}]",
                    layout_warnings,
                    is_root=False,
                    parent_type=node_type,
                )
            )
        repaired_node["children"] = repaired_children
        return repaired_node

    collected_warnings = list(repaired.get("warnings", [])) if isinstance(repaired.get("warnings"), list) else []
    repaired["layout"] = repair_node(repaired["layout"], "$.layout", collected_warnings, is_root=True)
    repaired["warnings"] = collected_warnings
    return repaired


def validate_or_repair_layout(layout_json: dict[str, Any], image_name: str) -> tuple[dict[str, Any], list[ValidationMessage], list[ValidationMessage], bool]:
    validation = validate_layout_document(layout_json)
    if validation.ok:
        return layout_json, validation.errors, validation.warnings, False

    repaired = repair_layout_json(layout_json, image_name)
    repaired_validation = validate_layout_document(repaired)
    repair_warning = make_message(
        "LAYOUT_REPAIRED",
        "Layout JSON was lightly repaired before final validation.",
        "$.layout",
    )

    if repaired_validation.ok:
        warnings = [repair_warning] + repaired_validation.warnings
        return repaired, repaired_validation.errors, warnings, True

    warnings = [repair_warning] + repaired_validation.warnings
    return repaired, repaired_validation.errors, warnings, True


def build_fallback_layout(image_name: str) -> tuple[dict[str, Any] | None, list[ValidationMessage], list[ValidationMessage]]:
    resolved = resolve_fallback_image_layout(image_name)
    errors = [make_message(item["code"], item["message"]) for item in resolved["errors"]]
    warnings = [make_message(item["code"], item["message"]) for item in resolved["warnings"]]
    if resolved["status"] != "SUCCESS" or not isinstance(resolved["layoutJson"], dict):
        return None, errors, warnings

    layout_json = copy.deepcopy(resolved["layoutJson"])
    layout_json["source"] = {
        "type": "screenshot",
        "fileUrl": None,
        "figmaFileKey": None,
        "figmaNodeId": None,
    }
    layout_json.setdefault("assumptions", []).append(
        {
            "target": layout_json["layout"]["id"],
            "message": f"Fallback template '{infer_template_key_from_image_name(image_name)}' was selected from the image name.",
        }
    )
    warnings.append(
        make_message(
            "FALLBACK_TEMPLATE_USED",
            f"Fallback template '{infer_template_key_from_image_name(image_name)}' was used.",
            "$.layout",
        )
    )
    return layout_json, errors, warnings


def compile_preview_html(
    layout_json: dict[str, Any],
) -> tuple[str, list[ValidationMessage], list[dict[str, str]]]:
    preview_html, compiler_warnings, unsupported_nodes, _, _ = compile_preview_document(layout_json)
    warnings = compiler_warnings[:]
    for node in unsupported_nodes:
        warnings.append(
            make_message(
                "UNSUPPORTED_NODE_RECORDED",
                f"Unsupported node skipped during preview compilation: {node['type']}",
                node["path"],
            )
        )
    return preview_html, warnings, unsupported_nodes


def infer_fallback_reason_from_ai_error(exc: Exception) -> str:
    message = str(exc).lower()
    if "did not contain valid json" in message or "non-json" in message:
        return FALLBACK_REASON_MODEL_NON_JSON_OUTPUT
    if "json" in message and "parse" in message:
        return FALLBACK_REASON_JSON_PARSE_FAILED
    if "image" in message and ("read" in message or "type" in message):
        return FALLBACK_REASON_IMAGE_READ_FAILED
    if "timeout" in message:
        return FALLBACK_REASON_WORKER_TIMEOUT
    return FALLBACK_REASON_MODEL_UNAVAILABLE


def process_image_layout_job(
    job_id: str,
    image_path: str | Path,
    mode: str,
    fallback: bool,
) -> tuple[dict[str, Any], int]:
    started_at = time.perf_counter()
    result_model = result_model_for_mode(mode)

    def finish(result: dict[str, Any], exit_code: int) -> tuple[dict[str, Any], int]:
        return add_runtime_metadata(result, started_at, result_model), exit_code

    fallback_reason: str | None = None
    validated_path, input_errors = validate_image_path(image_path)
    if input_errors:
        result = make_result(
            job_id=job_id,
            status="FAILED",
            mode=mode,
            fallback_used=False,
            source_type="IMAGE_FILE",
            layout_json=None,
            errors=input_errors,
            warnings=[],
            message="Input image path validation failed.",
            preview_html="",
            fallback_reason=FALLBACK_REASON_IMAGE_READ_FAILED,
        )
        return finish(result, 1)

    assert validated_path is not None
    image_name = validated_path.name

    if mode == "fallback-only":
        fallback_layout, fallback_errors, fallback_warnings = build_fallback_layout(image_name)
        if fallback_layout is None:
            result = make_result(
                job_id,
                "FAILED",
                mode,
                True,
                "FALLBACK_RULE",
                None,
                fallback_errors or [make_message("FALLBACK_LAYOUT_MISSING", "Fallback layout could not be created.")],
                fallback_warnings,
                "Fallback resolver failed.",
                "",
                fallback_reason=None,
            )
            return finish(result, 1)

        final_layout, errors, warnings, repaired = validate_or_repair_layout(fallback_layout, image_name)
        warnings = fallback_warnings + warnings
        message = "Fallback-only mode produced a validated Layout JSON."
        if repaired:
            message = "Fallback-only mode produced a repaired and validated Layout JSON."
        status = "SUCCESS" if not errors else "FAILED"
        preview_html = ""
        if status == "SUCCESS":
            preview_html, compiler_warnings, _ = compile_preview_html(final_layout)
            warnings = warnings + compiler_warnings
        result = make_result(
            job_id,
            status,
            mode,
            True,
            "FALLBACK_RULE",
            final_layout if status == "SUCCESS" else None,
            errors,
            warnings,
            message,
            preview_html,
            fallback_reason=None,
        )
        return finish(result, 0 if status == "SUCCESS" else 1)

    ai_warnings: list[ValidationMessage] = []
    try:
        intermediate = request_layout_intermediate(validated_path, job_id)
        intermediate, intermediate_repaired = repair_intermediate_payload(intermediate, image_name)
        if intermediate_repaired:
            ai_warnings.append(
                make_message(
                    "INTERMEDIATE_REPAIRED",
                    "AI intermediate payload was lightly repaired before layout mapping.",
                    "$.ai",
                )
            )
        candidate_layout = map_intermediate_to_layout_json(intermediate, image_name)
        final_layout, errors, warnings, repaired = validate_or_repair_layout(candidate_layout, image_name)
        all_warnings = ai_warnings + warnings
        if not errors:
            message = "Real AI produced a validated Layout JSON."
            if repaired:
                message = "Real AI produced a Layout JSON that required lightweight repair."
            preview_html, compiler_warnings, _ = compile_preview_html(final_layout)
            all_warnings = all_warnings + compiler_warnings
            result = make_result(
                job_id,
                "SUCCESS",
                mode,
                False,
                "REAL_AI",
                final_layout,
                errors,
                all_warnings,
                message,
                preview_html,
                fallback_reason=None,
            )
            return finish(result, 0)
        fallback_reason = FALLBACK_REASON_SCHEMA_VALIDATION_FAILED
        ai_warnings = all_warnings + [
            make_message("AI_LAYOUT_INVALID", "AI output could not pass validation without fallback.", "$.layout")
        ]
    except RealAIError as exc:
        fallback_reason = infer_fallback_reason_from_ai_error(exc)
        ai_warnings.append(make_message("REAL_AI_UNAVAILABLE", str(exc), "$.ai"))
    except Exception as exc:  # pragma: no cover - defensive path
        fallback_reason = FALLBACK_REASON_MODEL_UNAVAILABLE
        ai_warnings.append(make_message("REAL_AI_UNAVAILABLE", f"Unexpected AI error: {exc}", "$.ai"))

    if not fallback:
        result = make_result(
            job_id,
            "FAILED",
            mode,
            False,
            "REAL_AI",
            None,
            [make_message("REAL_AI_GENERATION_FAILED", "Real AI generation failed and fallback is disabled.", "$.ai")],
            ai_warnings,
            "Real AI generation failed and no fallback was allowed.",
            "",
            fallback_reason=fallback_reason,
        )
        return finish(result, 1)

    fallback_layout, fallback_errors, fallback_warnings = build_fallback_layout(image_name)
    if fallback_layout is None:
        errors = [make_message("FALLBACK_LAYOUT_MISSING", "Fallback layout could not be created.", "$.layout")]
        result = make_result(
            job_id,
            "FAILED",
            mode,
            True,
            "FALLBACK_RULE",
            None,
            fallback_errors + errors,
            ai_warnings + fallback_warnings,
            "Real AI failed and fallback layout could not be created.",
            "",
            fallback_reason=fallback_reason,
        )
        return finish(result, 1)

    final_layout, errors, warnings, repaired = validate_or_repair_layout(fallback_layout, image_name)
    combined_warnings = ai_warnings + fallback_warnings + warnings
    message = "Real AI failed, fallback resolver produced a validated Layout JSON."
    if repaired:
        message = "Real AI failed, fallback resolver produced a repaired and validated Layout JSON."
    status = "SUCCESS" if not errors else "FAILED"
    preview_html = ""
    if status == "SUCCESS":
        preview_html, compiler_warnings, _ = compile_preview_html(final_layout)
        combined_warnings = combined_warnings + compiler_warnings
    result = make_result(
        job_id,
        status,
        mode,
        True,
        "FALLBACK_RULE",
        final_layout if status == "SUCCESS" else None,
        errors,
        combined_warnings,
        message,
        preview_html,
        fallback_reason=fallback_reason,
    )
    return finish(result, 0 if status == "SUCCESS" else 1)
