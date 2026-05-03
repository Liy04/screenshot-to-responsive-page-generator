import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


LAYOUT_VERSION = "0.1"

TOP_LEVEL_REQUIRED = [
    "version",
    "page",
    "source",
    "tokens",
    "layout",
    "assets",
    "responsive",
    "assumptions",
    "warnings",
]

NODE_REQUIRED = [
    "id",
    "type",
    "role",
    "bounds",
    "style",
    "constraints",
    "interactions",
    "children",
]

NODE_TYPES = {
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

SOURCE_TYPES = {"manual", "screenshot", "figma"}
CONSTRAINT_VALUES = {"fixed", "fill", "hug", "center", "stretch"}


def configure_output_encoding() -> None:
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")


@dataclass
class ValidationMessage:
    code: str
    message: str
    path: str


@dataclass
class ValidationResult:
    errors: list[ValidationMessage]
    warnings: list[ValidationMessage]

    @property
    def ok(self) -> bool:
        return not self.errors


def load_json_file(file_path: str | Path) -> Any:
    path = Path(file_path)
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def validate_layout_document(document: Any) -> ValidationResult:
    errors: list[ValidationMessage] = []
    warnings: list[ValidationMessage] = []

    validate_schema(document, errors)
    if errors:
        return ValidationResult(errors=errors, warnings=warnings)

    nodes = collect_nodes(document["layout"])
    validate_business_rules(document, nodes, errors, warnings)

    return ValidationResult(errors=errors, warnings=warnings)


def validate_schema(document: Any, errors: list[ValidationMessage]) -> None:
    if not isinstance(document, dict):
        add_schema_error(errors, "document must be an object", "$")
        return

    for field in TOP_LEVEL_REQUIRED:
        if field not in document:
            add_schema_error(errors, f"missing required field '{field}'", f"$.{field}")

    if errors:
        return

    if document["version"] != LAYOUT_VERSION:
        add_schema_error(errors, "version must be '0.1'", "$.version")

    require_object(document["page"], "$.page", errors)
    require_object(document["source"], "$.source", errors)
    require_object(document["tokens"], "$.tokens", errors)
    require_object(document["layout"], "$.layout", errors)
    require_array(document["assets"], "$.assets", errors)
    require_object(document["responsive"], "$.responsive", errors)
    require_array(document["assumptions"], "$.assumptions", errors)
    require_array(document["warnings"], "$.warnings", errors)

    if errors:
        return

    validate_page_schema(document["page"], errors)
    validate_source_schema(document["source"], errors)
    validate_responsive_schema(document["responsive"], errors)
    validate_layout_node_schema(document["layout"], "$.layout", errors)


def validate_page_schema(page: dict[str, Any], errors: list[ValidationMessage]) -> None:
    for field in ["name", "type", "viewport"]:
        if field not in page:
            add_schema_error(errors, f"page missing required field '{field}'", f"$.page.{field}")

    if "name" in page and not isinstance(page["name"], str):
        add_schema_error(errors, "page.name must be a string", "$.page.name")
    if "type" in page and not isinstance(page["type"], str):
        add_schema_error(errors, "page.type must be a string", "$.page.type")
    if "viewport" not in page:
        return

    viewport = page["viewport"]
    if not require_object(viewport, "$.page.viewport", errors):
        return

    for field in ["width", "height"]:
        path = f"$.page.viewport.{field}"
        if field not in viewport:
            add_schema_error(errors, f"viewport missing required field '{field}'", path)
        elif not is_number(viewport[field]):
            add_schema_error(errors, f"viewport.{field} must be a number", path)


def validate_source_schema(source: dict[str, Any], errors: list[ValidationMessage]) -> None:
    if "type" not in source:
        add_schema_error(errors, "source missing required field 'type'", "$.source.type")
    elif source["type"] not in SOURCE_TYPES:
        add_schema_error(errors, "source.type is not supported", "$.source.type")

    for field in ["fileUrl", "figmaFileKey", "figmaNodeId"]:
        if field in source and not isinstance(source[field], (str, type(None))):
            add_schema_error(errors, f"source.{field} must be a string or null", f"$.source.{field}")


def validate_responsive_schema(responsive: dict[str, Any], errors: list[ValidationMessage]) -> None:
    for field in ["breakpoints", "rules"]:
        if field not in responsive:
            add_schema_error(errors, f"responsive missing required field '{field}'", f"$.responsive.{field}")

    if "breakpoints" in responsive and require_object(
        responsive["breakpoints"], "$.responsive.breakpoints", errors
    ):
        breakpoints = responsive["breakpoints"]
        for field in ["mobile", "tablet", "desktop"]:
            path = f"$.responsive.breakpoints.{field}"
            if field not in breakpoints:
                add_schema_error(errors, f"breakpoints missing required field '{field}'", path)
            elif not is_number(breakpoints[field]):
                add_schema_error(errors, f"breakpoints.{field} must be a number", path)

    if "rules" in responsive:
        require_array(responsive["rules"], "$.responsive.rules", errors)


def validate_layout_node_schema(node: Any, path: str, errors: list[ValidationMessage]) -> None:
    if not require_object(node, path, errors):
        return

    for field in NODE_REQUIRED:
        if field not in node:
            add_schema_error(errors, f"layout node missing required field '{field}'", f"{path}.{field}")

    if "id" in node and not isinstance(node["id"], str):
        add_schema_error(errors, "node.id must be a string", f"{path}.id")
    if "type" in node and node["type"] not in NODE_TYPES:
        add_schema_error(errors, "node.type is not supported", f"{path}.type")
    if "role" in node and not isinstance(node["role"], str):
        add_schema_error(errors, "node.role must be a string", f"{path}.role")
    if "content" in node and not isinstance(node["content"], str):
        add_schema_error(errors, "node.content must be a string", f"{path}.content")

    for field in ["src", "assetId"]:
        if field in node and not isinstance(node[field], (str, type(None))):
            add_schema_error(errors, f"node.{field} must be a string or null", f"{path}.{field}")

    if "bounds" in node:
        validate_bounds_schema(node["bounds"], f"{path}.bounds", errors)
    if "style" in node:
        require_object(node["style"], f"{path}.style", errors)
    if "constraints" in node:
        validate_constraints_schema(node["constraints"], f"{path}.constraints", errors)
    if "interactions" in node:
        require_array(node["interactions"], f"{path}.interactions", errors)
    if "dataBinding" in node:
        require_object(node["dataBinding"], f"{path}.dataBinding", errors)

    if "children" not in node:
        return
    if not require_array(node["children"], f"{path}.children", errors):
        return

    for index, child in enumerate(node["children"]):
        validate_layout_node_schema(child, f"{path}.children[{index}]", errors)


def validate_bounds_schema(bounds: Any, path: str, errors: list[ValidationMessage]) -> None:
    if not require_object(bounds, path, errors):
        return

    for field in ["x", "y", "width", "height"]:
        field_path = f"{path}.{field}"
        if field not in bounds:
            add_schema_error(errors, f"bounds missing required field '{field}'", field_path)
        elif not is_number(bounds[field]):
            add_schema_error(errors, f"bounds.{field} must be a number", field_path)


def validate_constraints_schema(constraints: Any, path: str, errors: list[ValidationMessage]) -> None:
    if not require_object(constraints, path, errors):
        return

    for field in ["horizontal", "vertical"]:
        field_path = f"{path}.{field}"
        if field not in constraints:
            add_schema_error(errors, f"constraints missing required field '{field}'", field_path)
        elif constraints[field] not in CONSTRAINT_VALUES:
            add_schema_error(errors, f"constraints.{field} is not supported", field_path)


def validate_business_rules(
    document: dict[str, Any],
    nodes: list[tuple[dict[str, Any], str]],
    errors: list[ValidationMessage],
    warnings: list[ValidationMessage],
) -> None:
    if document["layout"].get("type") != "page":
        errors.append(
            ValidationMessage(
                "ROOT_NODE_TYPE_INVALID",
                "layout 根节点 type 必须是 page",
                "$.layout.type",
            )
        )

    id_paths: dict[str, str] = {}
    for node, path in nodes:
        node_id = node["id"]
        if node_id in id_paths:
            errors.append(
                ValidationMessage(
                    "DUPLICATE_NODE_ID",
                    f"节点 id 重复: {node_id}",
                    path,
                )
            )
        else:
            id_paths[node_id] = path

        node_type = node["type"]
        if node_type == "text" and not has_content(node):
            errors.append(
                ValidationMessage("TEXT_CONTENT_MISSING", "text 节点必须有 content", path)
            )
        if node_type == "button" and not has_content(node):
            errors.append(
                ValidationMessage("BUTTON_CONTENT_MISSING", "button 节点必须有 content", path)
            )
        if node_type == "image" and not node.get("src") and not node.get("assetId"):
            warnings.append(
                ValidationMessage(
                    "IMAGE_SOURCE_MISSING",
                    "image 节点建议提供 src 或 assetId",
                    path,
                )
            )

        validate_style_token_warnings(document["tokens"], node.get("style", {}), path, warnings)

    for index, rule in enumerate(document["responsive"].get("rules", [])):
        if not isinstance(rule, dict):
            continue
        target = rule.get("target")
        if target is not None and target not in id_paths:
            errors.append(
                ValidationMessage(
                    "RESPONSIVE_TARGET_NOT_FOUND",
                    f"responsive.rules.target 不存在: {target}",
                    f"$.responsive.rules[{index}].target",
                )
            )

    for field in ["assumptions", "warnings"]:
        for index, item in enumerate(document.get(field, [])):
            if not isinstance(item, dict) or "target" not in item:
                continue
            target = item["target"]
            if target not in id_paths:
                warnings.append(
                    ValidationMessage(
                        "TARGET_NOT_FOUND",
                        f"{field}.target 不存在: {target}",
                        f"$.{field}[{index}].target",
                    )
                )


def validate_style_token_warnings(
    tokens: dict[str, Any],
    style: dict[str, Any],
    path: str,
    warnings: list[ValidationMessage],
) -> None:
    token_groups = {
        "background": "colors",
        "color": "colors",
        "typography": "typography",
        "spacing": "spacing",
        "radius": "radius",
    }
    for style_key, token_group in token_groups.items():
        if style_key not in style:
            continue
        value = style[style_key]
        group = tokens.get(token_group)
        if isinstance(value, str) and isinstance(group, dict) and value not in group:
            warnings.append(
                ValidationMessage(
                    "TOKEN_REFERENCE_NOT_FOUND",
                    f"style 引用了不存在的 token: {style_key}={value}",
                    f"{path}.style.{style_key}",
                )
            )


def collect_nodes(root: dict[str, Any]) -> list[tuple[dict[str, Any], str]]:
    nodes: list[tuple[dict[str, Any], str]] = []

    def walk(node: dict[str, Any], path: str) -> None:
        nodes.append((node, path))
        for index, child in enumerate(node.get("children", [])):
            walk(child, f"{path}.children[{index}]")

    walk(root, "$.layout")
    return nodes


def add_schema_error(errors: list[ValidationMessage], message: str, path: str) -> None:
    errors.append(ValidationMessage("SCHEMA_VALIDATION_ERROR", message, path))


def require_object(value: Any, path: str, errors: list[ValidationMessage]) -> bool:
    if not isinstance(value, dict):
        add_schema_error(errors, "must be an object", path)
        return False
    return True


def require_array(value: Any, path: str, errors: list[ValidationMessage]) -> bool:
    if not isinstance(value, list):
        add_schema_error(errors, "must be an array", path)
        return False
    return True


def is_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def has_content(node: dict[str, Any]) -> bool:
    content = node.get("content")
    return isinstance(content, str) and bool(content.strip())


def print_result(result: ValidationResult) -> None:
    if result.ok:
        print("校验通过")
    else:
        print("校验失败")
        for error in result.errors:
            print(f"[{error.code}] {error.message} {error.path}")

    if result.warnings:
        print("警告")
        for warning in result.warnings:
            print(f"[{warning.code}] {warning.message} {warning.path}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate Layout JSON v0.1 files.")
    parser.add_argument("layout_file", help="Path to a .layout.json file.")
    return parser.parse_args()


def main() -> int:
    configure_output_encoding()
    args = parse_args()
    try:
        document = load_json_file(args.layout_file)
    except FileNotFoundError:
        print("校验失败")
        print(f"[SCHEMA_VALIDATION_ERROR] 文件不存在 {args.layout_file}")
        return 1
    except json.JSONDecodeError as exc:
        print("校验失败")
        print(f"[SCHEMA_VALIDATION_ERROR] JSON 解析失败 line {exc.lineno} column {exc.colno}")
        return 1

    result = validate_layout_document(document)
    print_result(result)
    return 0 if result.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
