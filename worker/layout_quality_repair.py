import copy
from typing import Any


SECTION_ELEMENT_TYPES = {"text", "button", "input", "image", "card", "form", "container", "list", "listItem"}
SECTION_ELEMENT_TYPE_NAMES = {item.lower() for item in SECTION_ELEMENT_TYPES}
CONTAINER_ELEMENT_TYPES = {"card", "form", "container", "list", "listItem"}
FORM_ACTION_TEXTS = {
    "submit",
    "save",
    "send",
    "continue",
    "sign in",
    "log in",
    "login",
    "register",
    "create account",
    "apply",
    "confirm",
}
FORM_LABEL_KEYWORDS = {
    "label",
    "type",
    "note",
    "email",
    "password",
    "name",
    "message",
    "description",
    "phone",
    "address",
    "company",
    "project",
}


def normalize_intermediate_sections_for_quality(sections: Any) -> tuple[list[dict[str, Any]], bool]:
    if not isinstance(sections, list):
        return [], False

    normalized_sections: list[dict[str, Any]] = []
    changed = False

    for section in sections:
        if not isinstance(section, dict):
            changed = True
            continue

        normalized_section = normalize_intermediate_section(section)
        if normalized_section != section:
            changed = True
        normalized_sections.append(normalized_section)

    return normalized_sections, changed


def normalize_intermediate_section(section: dict[str, Any]) -> dict[str, Any]:
    normalized: dict[str, Any] = {}

    role = section.get("role")
    normalized["role"] = role.strip().lower() if isinstance(role, str) and role.strip() else "content"

    style = section.get("style")
    if isinstance(style, dict):
        normalized["style"] = copy.deepcopy(style)

    elements = section.get("elements")
    if not isinstance(elements, list):
        elements = section.get("components")
    normalized_elements = normalize_section_texts(section.get("texts")) + normalize_intermediate_elements(elements)
    normalized["elements"] = normalize_form_like_section_elements(normalized["role"], normalized_elements)

    nested_sections = section.get("sections")
    nested_normalized, _ = normalize_intermediate_sections_for_quality(nested_sections)
    if nested_normalized:
        normalized["sections"] = nested_normalized

    return normalized


def normalize_intermediate_elements(elements: Any) -> list[dict[str, Any]]:
    if not isinstance(elements, list):
        return []

    normalized: list[dict[str, Any]] = []
    for element in elements:
        normalized_element = normalize_intermediate_element(element)
        if normalized_element is not None:
            normalized.append(normalized_element)
    return normalized


def normalize_form_like_section_elements(role: str, elements: list[dict[str, Any]]) -> list[dict[str, Any]]:
    if not elements or any(element.get("type") == "form" for element in elements):
        return elements
    if not is_form_like_section(role, elements):
        return elements

    leading: list[dict[str, Any]] = []
    candidates = elements
    first_content = element_content(elements[0]) if elements else None
    if (
        len(elements) > 2
        and elements[0].get("type") == "text"
        and elements[0].get("role") in {"heading", "title"}
        and first_content is not None
        and not is_form_label_text(first_content)
    ):
        leading = [elements[0]]
        candidates = elements[1:]

    form_children = form_children_from_plain_rows(candidates)
    if not has_form_control(form_children):
        return elements

    return leading + [{"type": "form", "role": "form", "elements": form_children}]


def form_children_from_plain_rows(elements: list[dict[str, Any]]) -> list[dict[str, Any]]:
    children: list[dict[str, Any]] = []
    index = 0
    while index < len(elements):
        element = elements[index]
        content = element_content(element)
        if content is None:
            index += 1
            continue

        if is_action_element(element):
            children.append({"type": "button", "role": "primary-action", "content": content})
            index += 1
            continue

        if element.get("type") == "input":
            label = first_non_empty_string(element, ("label", "content", "text")) or content
            children.append({"type": "text", "role": "label", "content": label})
            children.append({"type": "input", "role": "field", "content": content, "label": label})
            index += 1
            continue

        if is_form_label_text(content):
            children.append({"type": "text", "role": "label", "content": content})
            values = collect_form_values(elements, index + 1)
            if not values:
                children.append({"type": "input", "role": "field", "content": content, "label": content})
                index += 1
                continue
            if len(values) == 1:
                children.append({"type": "input", "role": "field", "content": values[0], "label": content})
            else:
                for value in values:
                    children.append({"type": "button", "role": "secondary-action", "content": value})
            index += 1 + len(values)
            continue

        children.append({"type": "input", "role": "field", "content": content})
        index += 1
    return children


def collect_form_values(elements: list[dict[str, Any]], start_index: int) -> list[str]:
    values: list[str] = []
    index = start_index
    while index < len(elements):
        element = elements[index]
        content = element_content(element)
        if content is None or is_action_element(element) or is_form_label_text(content):
            break
        values.append(content)
        index += 1
        if len(values) >= 3:
            break
    return values


def is_form_like_section(role: str, elements: list[dict[str, Any]]) -> bool:
    normalized_role = role.strip().lower()
    has_input = any(element.get("type") == "input" for element in elements)
    has_action = any(is_action_element(element) for element in elements)
    has_label = any(is_form_label_text(content) for content in element_contents(elements))
    return normalized_role == "form" or (has_action and (has_label or has_input))


def has_form_control(elements: list[dict[str, Any]]) -> bool:
    return any(element.get("type") in {"input", "button"} for element in elements)


def element_contents(elements: list[dict[str, Any]]) -> list[str]:
    contents: list[str] = []
    for element in elements:
        content = element_content(element)
        if content is not None:
            contents.append(content)
    return contents


def element_content(element: dict[str, Any]) -> str | None:
    return first_non_empty_string(element, ("content", "label", "text"))


def is_action_element(element: dict[str, Any]) -> bool:
    role = str(element.get("role", "")).strip().lower()
    content = element_content(element)
    return element.get("type") == "button" or "action" in role or role == "submit" or is_action_text(content)


def is_action_text(content: str | None) -> bool:
    if content is None:
        return False
    normalized = content.strip().lower()
    return normalized in FORM_ACTION_TEXTS


def is_form_label_text(content: str) -> bool:
    normalized = content.strip().lower()
    if not normalized:
        return False
    return any(keyword in normalized for keyword in FORM_LABEL_KEYWORDS)


def normalize_section_texts(texts: Any) -> list[dict[str, str]]:
    if not isinstance(texts, list):
        return []

    normalized: list[dict[str, str]] = []
    seen: set[str] = set()
    for value in texts:
        if not isinstance(value, str):
            continue
        content = value.strip()
        if not content:
            continue
        key = content.lower()
        if key in seen:
            continue
        seen.add(key)
        normalized.append(
            {
                "type": "text",
                "role": "heading" if not normalized else "body",
                "content": content,
            }
        )
    return normalized


def normalize_intermediate_element(element: Any) -> dict[str, Any] | None:
    if isinstance(element, str):
        content = element.strip()
        if not content:
            return None
        return {"type": "text", "role": "body", "content": content}

    if not isinstance(element, dict):
        return None

    raw_type = str(element.get("type", "text")).strip() or "text"
    node_type = normalize_element_type(raw_type)
    role = str(element.get("role", default_role_for_type(node_type))).strip() or default_role_for_type(node_type)
    normalized: dict[str, Any] = {"type": node_type, "role": role}

    content = first_non_empty_string(element, ("content", "text", "label"))
    if content is not None:
        normalized["content"] = content
    if node_type == "input":
        label = first_non_empty_string(element, ("label", "content", "text"))
        if label is not None:
            normalized["label"] = label

    style = element.get("style")
    if isinstance(style, dict):
        normalized["style"] = copy.deepcopy(style)

    nested = first_list(element, ("elements", "items", "children"))
    nested_elements = normalize_intermediate_elements(nested)
    if node_type in CONTAINER_ELEMENT_TYPES and nested_elements:
        normalized["elements"] = nested_elements

    if node_type == "form":
        normalized.setdefault("elements", nested_elements)
        return normalized
    if node_type in CONTAINER_ELEMENT_TYPES:
        return normalized if content is not None or nested_elements else None
    if node_type in {"text", "button", "input"}:
        return normalized if content is not None or node_type == "input" else None
    if node_type == "image":
        return normalized
    return None


def normalize_element_type(raw_type: str) -> str:
    normalized = raw_type.strip()
    lowered = normalized.lower()
    if lowered == "listitem":
        return "listItem"
    if lowered in SECTION_ELEMENT_TYPE_NAMES:
        return lowered
    return "text"


def default_role_for_type(node_type: str) -> str:
    if node_type == "button":
        return "primary-action"
    if node_type == "input":
        return "field"
    if node_type == "card":
        return "card"
    if node_type == "form":
        return "form"
    return "body"


def first_non_empty_string(values: dict[str, Any], keys: tuple[str, ...]) -> str | None:
    for key in keys:
        value = values.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    return None


def first_list(values: dict[str, Any], keys: tuple[str, ...]) -> list[Any] | None:
    for key in keys:
        value = values.get(key)
        if isinstance(value, list):
            return value
    return None
