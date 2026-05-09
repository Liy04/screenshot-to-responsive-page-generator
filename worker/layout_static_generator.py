import argparse
import hashlib
import html
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    from .layout_validator import (
        ValidationMessage,
        configure_output_encoding,
        load_json_file,
        validate_layout_document,
    )
except ImportError:
    from layout_validator import (
        ValidationMessage,
        configure_output_encoding,
        load_json_file,
        validate_layout_document,
    )


ARTIFACT_VERSION = "0.1"
GENERATOR_NAME = "layout-static-generator"
GENERATOR_VERSION = "0.1"

STYLE_PROPERTIES = {
    "width": "width",
    "height": "height",
    "maxWidth": "max-width",
    "backgroundColor": "background-color",
    "color": "color",
    "fontSize": "font-size",
    "lineHeight": "line-height",
    "fontWeight": "font-weight",
    "borderRadius": "border-radius",
    "padding": "padding",
    "margin": "margin",
    "textAlign": "text-align",
    "display": "display",
    "flexDirection": "flex-direction",
    "gap": "gap",
    "objectFit": "object-fit",
    "justifyContent": "justify-content",
    "alignItems": "align-items",
}

BASE_CLASSES = {
    "page": ("div", "lg-page"),
    "section": ("section", "lg-section"),
    "container": ("div", "lg-container"),
    "button": ("button", "lg-button"),
    "image": ("img", "lg-image"),
    "card": ("div", "lg-card"),
    "list": ("ul", "lg-list"),
    "listItem": ("li", "lg-list-item"),
    "form": ("form", "lg-form"),
    "input": ("input", "lg-input"),
}

VOID_TAGS = {"img", "input"}
SAFE_COLOR_NAMES = {
    "black",
    "white",
    "red",
    "green",
    "blue",
    "gray",
    "grey",
    "transparent",
    "currentColor",
}
SAFE_DISPLAY_VALUES = {"block", "inline-block", "flex", "grid", "none"}
SAFE_FLEX_DIRECTIONS = {"row", "row-reverse", "column", "column-reverse"}
SAFE_TEXT_ALIGN_VALUES = {"left", "right", "center", "justify", "start", "end"}
SAFE_OBJECT_FIT_VALUES = {"fill", "contain", "cover", "none", "scale-down"}
SAFE_ALIGN_VALUES = {
    "flex-start",
    "flex-end",
    "center",
    "space-between",
    "space-around",
    "space-evenly",
    "stretch",
    "baseline",
}


def message_to_dict(message: ValidationMessage) -> dict[str, str]:
    return {
        "code": message.code,
        "message": message.message,
        "path": message.path,
    }


def make_message(code: str, message: str, path: str) -> ValidationMessage:
    return ValidationMessage(code=code, message=message, path=path)


def stable_layout_hash(document: Any) -> str:
    normalized = json.dumps(document, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()


def make_failed_artifact(
    document: Any | None,
    errors: list[ValidationMessage],
    warnings: list[ValidationMessage] | None = None,
) -> dict[str, Any]:
    warnings = warnings or []
    return make_artifact(
        document=document,
        status="FAILED",
        errors=errors,
        warnings=warnings,
        html_code="",
        css_code="",
        vue_code="",
        unsupported_nodes=[],
    )


def make_success_artifact(
    document: dict[str, Any],
    warnings: list[ValidationMessage],
    html_code: str,
    css_code: str,
    vue_code: str,
    unsupported_nodes: list[dict[str, str]],
) -> dict[str, Any]:
    return make_artifact(
        document=document,
        status="SUCCESS",
        errors=[],
        warnings=warnings,
        html_code=html_code,
        css_code=css_code,
        vue_code=vue_code,
        unsupported_nodes=unsupported_nodes,
    )


def make_artifact(
    document: Any | None,
    status: str,
    errors: list[ValidationMessage],
    warnings: list[ValidationMessage],
    html_code: str,
    css_code: str,
    vue_code: str,
    unsupported_nodes: list[dict[str, str]],
) -> dict[str, Any]:
    layout_hash = stable_layout_hash(document) if document is not None else ""
    source = document.get("source", {}) if isinstance(document, dict) else {}
    return {
        "version": ARTIFACT_VERSION,
        "artifactType": "generated-page",
        "jobId": make_job_id(layout_hash),
        "generator": {
            "name": GENERATOR_NAME,
            "version": GENERATOR_VERSION,
        },
        "source": {
            "layoutVersion": document.get("version", "") if isinstance(document, dict) else "",
            "layoutHash": layout_hash,
            "layoutSourceType": source.get("type", "unknown"),
        },
        "validation": {
            "passed": not errors,
            "errors": [message_to_dict(error) for error in errors],
            "warnings": [message_to_dict(warning) for warning in warnings],
        },
        "status": status,
        "htmlCode": html_code,
        "cssCode": css_code,
        "vueCode": vue_code,
        "unsupportedNodes": unsupported_nodes,
        "createdAt": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
    }


def make_job_id(layout_hash: str) -> str:
    if not layout_hash:
        return "job-invalid-layout"
    return f"job-{layout_hash[:12]}"


def compile_document(document: dict[str, Any]) -> tuple[str, str, str, list[ValidationMessage], list[dict[str, str]]]:
    warnings: list[ValidationMessage] = []
    unsupported_nodes: list[dict[str, str]] = []
    css_blocks = base_css_blocks()
    html_code = compile_node(document["layout"], "$.layout", css_blocks, warnings, unsupported_nodes)
    css_code = "\n\n".join(css_blocks)
    vue_code = make_vue_text(html_code, css_code)
    return html_code, css_code, vue_code, warnings, unsupported_nodes


def compile_node(
    node: dict[str, Any],
    path: str,
    css_blocks: list[str],
    warnings: list[ValidationMessage],
    unsupported_nodes: list[dict[str, str]],
) -> str:
    node_type = node.get("type", "")
    tag, base_class = node_mapping(node)
    if tag is None:
        unsupported_nodes.append(
            {
                "id": str(node.get("id", "")),
                "type": str(node_type),
                "path": path,
            }
        )
        warnings.append(
            make_message("UNSUPPORTED_NODE_TYPE", f"node type 暂不支持: {node_type}", f"{path}.type")
        )
        return ""

    node_class = make_node_class(str(node.get("id", "")))
    class_attr = html.escape(f"{base_class} {node_class}", quote=True)
    style_css = compile_style(node.get("style", {}), f"{path}.style", warnings)
    if style_css:
        css_blocks.append(f".{node_class} {{\n{style_css}\n}}")

    children_html = "".join(
        compile_node(child, f"{path}.children[{index}]", css_blocks, warnings, unsupported_nodes)
        for index, child in enumerate(node.get("children", []))
    )

    if node_type == "text":
        content = html.escape(str(node.get("content", "")), quote=False)
        return f'<{tag} class="{class_attr}">{content}{children_html}</{tag}>'

    if node_type == "button":
        content = html.escape(str(node.get("content", "")), quote=False)
        return f'<button class="{class_attr}" type="button">{content}{children_html}</button>'

    if node_type == "image":
        src_attr = make_image_src_attr(node, path, warnings)
        return f'<img class="{class_attr}"{src_attr} alt="" />'

    if node_type == "input":
        return f'<input class="{class_attr}" type="text" />'

    if tag in VOID_TAGS:
        return f'<{tag} class="{class_attr}" />'

    return f'<{tag} class="{class_attr}">{children_html}</{tag}>'


def node_mapping(node: dict[str, Any]) -> tuple[str | None, str]:
    node_type = node.get("type")
    if node_type == "text":
        return text_tag_for_node(node), "lg-text"
    return BASE_CLASSES.get(str(node_type), (None, ""))


def text_tag_for_node(node: dict[str, Any]) -> str:
    role = str(node.get("role", "")).lower()
    level = node.get("level")
    if level == 1 or role in {"heading", "title"}:
        return "h1"
    if level == 2 or role in {"subheading", "sectionheading"}:
        return "h2"
    if role in {"label", "metric"}:
        return "span"
    return "p"


def make_node_class(node_id: str) -> str:
    safe = re.sub(r"[^A-Za-z0-9_-]+", "-", node_id).strip("-")
    if not safe:
        safe = "node"
    return f"lg-node-{safe}"


def make_image_src_attr(node: dict[str, Any], path: str, warnings: list[ValidationMessage]) -> str:
    src = node.get("src")
    if not isinstance(src, str) or not is_safe_image_src(src):
        warnings.append(
            make_message("IMAGE_SAFE_SRC_MISSING", "image 缺少安全 src，已跳过 src 属性", f"{path}.src")
        )
        return ""
    return f' src="{html.escape(src, quote=True)}"'


def is_safe_image_src(src: str) -> bool:
    stripped = src.strip()
    lowered = stripped.lower()
    if not stripped:
        return False
    if lowered.startswith(("javascript:", "data:")):
        return False
    if "<" in stripped or ">" in stripped:
        return False
    if "../" in stripped or stripped.startswith(".."):
        return False
    if lowered.startswith(("http://", "https://")):
        return True
    if stripped.startswith("/uploads/"):
        return True
    return not stripped.startswith("/")


def compile_style(
    style: Any,
    path: str,
    warnings: list[ValidationMessage],
) -> str:
    if not isinstance(style, dict):
        return ""

    lines: list[str] = []
    for key in sorted(style):
        value = style[key]
        if key not in STYLE_PROPERTIES:
            warnings.append(make_message("UNKNOWN_STYLE_FIELD", "style 字段暂不支持", f"{path}.{key}"))
            continue

        css_value = safe_css_value(key, value)
        if css_value is None:
            warnings.append(
                make_message("UNSAFE_CSS_VALUE", f"CSS 值不安全或不支持: {key}", f"{path}.{key}")
            )
            continue
        lines.append(f"  {STYLE_PROPERTIES[key]}: {css_value};")

    return "\n".join(lines)


def safe_css_value(key: str, value: Any) -> str | None:
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        if key in {"width", "height", "maxWidth", "fontSize", "borderRadius", "padding", "margin", "gap"}:
            return f"{value}px"
        if key == "lineHeight":
            return str(value)
        if key == "fontWeight":
            return str(value) if value in range(100, 1000, 100) else None
        return None

    if not isinstance(value, str):
        return None

    stripped = value.strip()
    lowered = stripped.lower()
    if not stripped:
        return None
    if any(token in lowered for token in ["url(", "expression(", "javascript:"]):
        return None
    if "<" in stripped or ">" in stripped:
        return None

    if key in {"backgroundColor", "color"}:
        return stripped if is_safe_color(stripped) else None
    if key in {"width", "height", "maxWidth", "fontSize", "borderRadius", "padding", "margin", "gap"}:
        return stripped if is_safe_length(stripped) else None
    if key == "lineHeight":
        return stripped if is_safe_line_height(stripped) else None
    if key == "fontWeight":
        return stripped if is_safe_font_weight(stripped) else None
    if key == "textAlign":
        return stripped if stripped in SAFE_TEXT_ALIGN_VALUES else None
    if key == "display":
        return stripped if stripped in SAFE_DISPLAY_VALUES else None
    if key == "flexDirection":
        return stripped if stripped in SAFE_FLEX_DIRECTIONS else None
    if key == "objectFit":
        return stripped if stripped in SAFE_OBJECT_FIT_VALUES else None
    if key in {"justifyContent", "alignItems"}:
        return stripped if stripped in SAFE_ALIGN_VALUES else None
    return None


def is_safe_color(value: str) -> bool:
    if value in SAFE_COLOR_NAMES:
        return True
    if re.fullmatch(r"#[0-9A-Fa-f]{3}([0-9A-Fa-f]{3})?", value):
        return True
    if re.fullmatch(r"rgba?\(\s*\d{1,3}\s*,\s*\d{1,3}\s*,\s*\d{1,3}(\s*,\s*(0|1|0?\.\d+))?\s*\)", value):
        return True
    return False


def is_safe_length(value: str) -> bool:
    return bool(re.fullmatch(r"-?\d+(\.\d+)?(px|rem|em|%)", value))


def is_safe_font_weight(value: str) -> bool:
    return value in {"normal", "bold"} or bool(re.fullmatch(r"[1-9]00", value))


def is_safe_line_height(value: str) -> bool:
    if re.fullmatch(r"\d+(\.\d+)?", value):
        return True
    return is_safe_length(value)


def base_css_blocks() -> list[str]:
    return [
        "\n".join(
            [
                ".lg-page {",
                "  box-sizing: border-box;",
                "  width: 100%;",
                "  min-height: 100vh;",
                "  font-family: Arial, sans-serif;",
                "}",
                ".lg-page *, .lg-page *::before, .lg-page *::after {",
                "  box-sizing: border-box;",
                "}",
            ]
        ),
        "\n".join(
            [
                ".lg-section, .lg-container, .lg-card, .lg-form {",
                "  display: flex;",
                "  flex-direction: column;",
                "}",
                ".lg-button {",
                "  cursor: pointer;",
                "}",
                ".lg-image {",
                "  max-width: 100%;",
                "  height: auto;",
                "}",
                ".lg-list {",
                "  list-style: none;",
                "  margin: 0;",
                "  padding: 0;",
                "}",
            ]
        ),
    ]


def make_vue_text(html_code: str, css_code: str) -> str:
    return "\n".join(
        [
            "<template>",
            html_code,
            "</template>",
            "",
            "<style scoped>",
            css_code,
            "</style>",
        ]
    )


def generate_artifact(file_path: str | Path) -> tuple[dict[str, Any], int]:
    try:
        document = load_json_file(file_path)
    except FileNotFoundError:
        error = make_message("SCHEMA_VALIDATION_ERROR", "文件不存在", str(file_path))
        return make_failed_artifact(None, [error]), 1
    except json.JSONDecodeError as exc:
        error = make_message(
            "SCHEMA_VALIDATION_ERROR",
            f"JSON 解析失败 line {exc.lineno} column {exc.colno}",
            str(file_path),
        )
        return make_failed_artifact(None, [error]), 1

    validation = validate_layout_document(document)
    if not validation.ok:
        return make_failed_artifact(document, validation.errors, validation.warnings), 1

    html_code, css_code, vue_code, generator_warnings, unsupported_nodes = compile_document(document)
    warnings = validation.warnings + generator_warnings
    artifact = make_success_artifact(
        document,
        warnings,
        html_code,
        css_code,
        vue_code,
        unsupported_nodes,
    )
    return artifact, 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Compile Layout JSON v0.1 to generated-page artifact.")
    parser.add_argument("layout_file", help="Path to a .layout.json file.")
    return parser.parse_args()


def main() -> int:
    configure_output_encoding()
    args = parse_args()
    artifact, exit_code = generate_artifact(args.layout_file)
    print(json.dumps(artifact, ensure_ascii=False, indent=2))
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
