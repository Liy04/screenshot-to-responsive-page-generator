import copy
from pathlib import Path
from typing import Any

try:
    from .layout_static_generator import compile_preview_document
    from .image_layout_resolver import infer_template_key_from_image_name, resolve_fallback_image_layout
    from .layout_validator import ValidationMessage, validate_layout_document
    from .real_ai_layout_client import PROMPT_VERSION, RealAIError, request_layout_intermediate
except ImportError:
    from layout_static_generator import compile_preview_document
    from image_layout_resolver import infer_template_key_from_image_name, resolve_fallback_image_layout
    from layout_validator import ValidationMessage, validate_layout_document
    from real_ai_layout_client import PROMPT_VERSION, RealAIError, request_layout_intermediate


ALLOWED_IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg", ".webp"}
MAX_IMAGE_SIZE_BYTES = 5 * 1024 * 1024
FALLBACK_REASON_MODEL_UNAVAILABLE = "MODEL_UNAVAILABLE"
FALLBACK_REASON_MODEL_NON_JSON_OUTPUT = "MODEL_NON_JSON_OUTPUT"
FALLBACK_REASON_JSON_PARSE_FAILED = "JSON_PARSE_FAILED"
FALLBACK_REASON_SCHEMA_VALIDATION_FAILED = "SCHEMA_VALIDATION_FAILED"
FALLBACK_REASON_IMAGE_READ_FAILED = "IMAGE_READ_FAILED"
FALLBACK_REASON_WORKER_TIMEOUT = "WORKER_TIMEOUT"
FALLBACK_REASON_PREVIEW_COMPILE_FAILED = "PREVIEW_COMPILE_FAILED"


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


def infer_children_from_section(section: dict[str, Any], start_y: int, assets: list[dict[str, Any]]) -> list[dict[str, Any]]:
    elements = section.get("elements")
    if not isinstance(elements, list):
        elements = []

    children: list[dict[str, Any]] = []
    cursor_y = start_y
    for index, element in enumerate(elements):
        if not isinstance(element, dict):
            continue
        node_type = str(element.get("type", "text"))
        role = str(element.get("role", "content"))
        node_id = f"ai-section-{start_y}-node-{index}"
        node: dict[str, Any] = {
            "id": node_id,
            "type": node_type if node_type in {"text", "button", "image", "container", "card", "list", "listItem", "input"} else "text",
            "role": role,
            "bounds": default_bounds(120, cursor_y, 440, 48),
            "style": {},
            "constraints": default_constraints(),
            "interactions": [],
            "children": [],
        }

        if node["type"] in {"text", "button"}:
            content = element.get("content")
            node["content"] = content if isinstance(content, str) and content.strip() else f"{role} {index + 1}"
        elif node["type"] == "image":
            asset_id = f"ai-image-asset-{index + 1}"
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
                "style": {},
                "constraints": default_constraints(),
                "interactions": [],
                "children": [],
            }
        )

    return children


def map_intermediate_to_layout_json(intermediate: dict[str, Any], image_name: str) -> dict[str, Any]:
    page_name = intermediate.get("pageName")
    if not isinstance(page_name, str) or not page_name.strip():
        page_name = default_page_name(image_name)

    page_type = normalize_page_type(intermediate.get("pageType"))
    sections = intermediate.get("sections")
    if not isinstance(sections, list):
        sections = []

    assets: list[dict[str, Any]] = []
    layout_sections: list[dict[str, Any]] = []
    section_y = 80

    if not sections:
        sections = [{"role": "content", "elements": [{"type": "text", "role": "heading", "content": page_name}]}]

    for index, section in enumerate(sections):
        if not isinstance(section, dict):
            continue
        role = str(section.get("role", f"section{index + 1}"))
        children = infer_children_from_section(section, section_y + 32, assets)
        section_height = max(220, 72 * max(len(children), 1) + 64)
        layout_sections.append(
            {
                "id": f"ai-section-{index + 1}",
                "type": "section",
                "role": role,
                "bounds": default_bounds(80, section_y, 1280, section_height),
                "style": {},
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
            "style": {},
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
        "warnings": [],
    }


def repair_intermediate_payload(intermediate: Any, image_name: str) -> tuple[dict[str, Any], bool]:
    if not isinstance(intermediate, dict):
        return {}, False

    repaired = copy.deepcopy(intermediate)
    used = False

    page_name = repaired.get("pageName")
    if not isinstance(page_name, str) or not page_name.strip():
        repaired["pageName"] = default_page_name(image_name)
        used = True

    page_type = repaired.get("pageType")
    if not isinstance(page_type, str) or not page_type.strip():
        repaired["pageType"] = "generic"
        used = True

    sections = repaired.get("sections")
    if not isinstance(sections, list):
        repaired["sections"] = []
        sections = repaired["sections"]
        used = True

    normalized_sections: list[dict[str, Any]] = []
    sections_changed = False
    for section in sections:
        if not isinstance(section, dict):
            sections_changed = True
            continue

        normalized_section = copy.deepcopy(section)
        role = normalized_section.get("role")
        if not isinstance(role, str) or not role.strip():
            normalized_section["role"] = "content"
            sections_changed = True

        elements = normalized_section.get("elements")
        if not isinstance(elements, list):
            normalized_section["elements"] = []
            sections_changed = True

        normalized_sections.append(normalized_section)

    if sections_changed:
        repaired["sections"] = normalized_sections
        used = True

    return repaired, used


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
        repaired["layout"] = {
            "id": "repaired-root",
            "type": "page",
            "role": "page",
            "bounds": default_bounds(0, 0, 1440, 900),
            "style": {},
            "constraints": default_constraints("fill", "fill"),
            "interactions": [],
            "children": [],
        }
    else:
        layout.setdefault("id", "repaired-root")
        layout.setdefault("type", "page")
        layout.setdefault("role", "page")
        layout.setdefault("bounds", default_bounds(0, 0, 1440, 900))
        layout.setdefault("style", {})
        layout.setdefault("constraints", default_constraints("fill", "fill"))
        layout.setdefault("interactions", [])
        layout.setdefault("children", [])
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
        return result, 1

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
            return result, 1

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
        return result, 0 if status == "SUCCESS" else 1

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
            return result, 0
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
        return result, 1

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
        return result, 1

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
    return result, 0 if status == "SUCCESS" else 1
