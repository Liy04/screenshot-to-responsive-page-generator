import base64
import json
import os
import re
from pathlib import Path
from typing import Any

try:
    from openai import OpenAI
except ImportError:  # pragma: no cover - environment dependent
    OpenAI = None


DEFAULT_OPENAI_MODEL = "gpt-4.1-mini"
PROMPT_VERSION = "week10-v1"


class RealAIError(RuntimeError):
    pass


class RealAIUnavailableError(RealAIError):
    pass


class RealAIResponseError(RealAIError):
    pass


def detect_image_mime_type(image_path: Path) -> str:
    suffix = image_path.suffix.lower()
    if suffix == ".png":
        return "image/png"
    if suffix in {".jpg", ".jpeg"}:
        return "image/jpeg"
    if suffix == ".webp":
        return "image/webp"
    raise RealAIResponseError(f"Unsupported image type: {suffix}")


def build_prompt(job_id: str, image_name: str) -> str:
    return "\n".join(
        [
            "You are a layout extraction assistant.",
            "Look at the provided webpage screenshot and return JSON only.",
            "Do not return markdown or prose.",
            f"Prompt version: {PROMPT_VERSION}",
            "Target schema for your JSON output:",
            "{",
            '  "pageName": "string",',
            '  "pageType": "marketing|dashboard|auth|profile|mobile-list|generic",',
            '  "sections": [',
            "    {",
            '      "role": "hero|header|content|footer|summary|form|list",',
            '      "elements": [',
            "        {",
            '          "type": "text|button|image|container|card|list|listItem|input",',
            '          "role": "string",',
            '          "content": "optional string"',
            "        }",
            "      ]",
            "    }",
            "  ]",
            "}",
            f"Job ID: {job_id}",
            f"Image name: {image_name}",
        ]
    )


def image_path_to_data_url(image_path: Path) -> str:
    mime_type = detect_image_mime_type(image_path)
    raw = image_path.read_bytes()
    encoded = base64.b64encode(raw).decode("ascii")
    return f"data:{mime_type};base64,{encoded}"


def parse_json_object(candidate: str) -> dict[str, Any]:
    parsed = json.loads(candidate)
    if not isinstance(parsed, dict):
        raise RealAIResponseError("Model output JSON must be an object")
    return parsed


def find_first_json_object(text: str) -> dict[str, Any] | None:
    for start_index, char in enumerate(text):
        if char != "{":
            continue

        depth = 0
        in_string = False
        escape = False
        for end_index in range(start_index, len(text)):
            current = text[end_index]
            if in_string:
                if escape:
                    escape = False
                elif current == "\\":
                    escape = True
                elif current == '"':
                    in_string = False
                continue

            if current == '"':
                in_string = True
                continue

            if current == "{":
                depth += 1
                continue

            if current == "}":
                depth -= 1
                if depth == 0:
                    candidate = text[start_index : end_index + 1]
                    try:
                        return parse_json_object(candidate)
                    except (json.JSONDecodeError, RealAIResponseError):
                        break
    return None


def parse_json_payload(text: str) -> dict[str, Any]:
    stripped = text.strip()
    if not stripped:
        raise RealAIResponseError("Model returned empty text output")

    try:
        return parse_json_object(stripped)
    except json.JSONDecodeError:
        pass

    fenced_blocks = re.findall(r"```(?:json)?\s*(.*?)\s*```", stripped, re.DOTALL | re.IGNORECASE)
    for block in fenced_blocks:
        candidate = block.strip()
        if not candidate:
            continue
        try:
            return parse_json_object(candidate)
        except json.JSONDecodeError:
            nested = find_first_json_object(candidate)
            if nested is not None:
                return nested
        except RealAIResponseError:
            nested = find_first_json_object(candidate)
            if nested is not None:
                return nested

    extracted = find_first_json_object(stripped)
    if extracted is not None:
        return extracted

    raise RealAIResponseError("Model output did not contain valid JSON")


def build_openai_client() -> Any:
    if OpenAI is None:
        raise RealAIUnavailableError("openai package is not available in this environment")

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RealAIUnavailableError("OPENAI_API_KEY is not set")

    base_url = os.getenv("OPENAI_BASE_URL")
    if base_url:
        return OpenAI(api_key=api_key, base_url=base_url)
    return OpenAI(api_key=api_key)


def extract_chat_completion_text(response: Any) -> str:
    choices = getattr(response, "choices", None)
    if not choices:
        raise RealAIResponseError("Model response did not contain choices")

    message = getattr(choices[0], "message", None)
    if message is None:
        raise RealAIResponseError("Model response did not contain a message")

    content = getattr(message, "content", "")
    if isinstance(content, str):
        return content

    if isinstance(content, list):
        texts: list[str] = []
        for item in content:
            if isinstance(item, str):
                texts.append(item)
                continue
            if isinstance(item, dict):
                text_value = item.get("text")
                if isinstance(text_value, str):
                    texts.append(text_value)
                continue
            text_value = getattr(item, "text", None)
            if isinstance(text_value, str):
                texts.append(text_value)
        if texts:
            return "\n".join(texts)

    raise RealAIResponseError("Model response did not contain text content")


def request_layout_intermediate(image_path: str | Path, job_id: str) -> dict[str, Any]:
    image_path = Path(image_path)
    model = os.getenv("OPENAI_MODEL", DEFAULT_OPENAI_MODEL)
    client = build_openai_client()
    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": build_prompt(job_id, image_path.name),
                    },
                    {
                        "type": "image_url",
                        "image_url": {"url": image_path_to_data_url(image_path)},
                    },
                ],
            }
        ],
    )

    output_text = extract_chat_completion_text(response)
    return parse_json_payload(output_text)
