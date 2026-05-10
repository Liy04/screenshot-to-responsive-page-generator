import argparse
import json
import sys
from pathlib import Path
from typing import Any


SOURCE_TYPE = "IMAGE_TEMPLATE_MOCK"
FIXTURE_DIR = Path(__file__).resolve().parent / "fixtures" / "image_templates"
TEMPLATE_FIXTURES = {
    "landing-basic": "landing-basic.layout.json",
    "card-list": "card-list.layout.json",
    "invalid-layout": "invalid-layout.layout.json",
}


def configure_output_encoding() -> None:
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")


def build_source(template_key: str, image_name: str) -> dict[str, str]:
    return {
        "type": SOURCE_TYPE,
        "templateKey": template_key,
        "imageName": image_name,
    }


def make_error(code: str, message: str) -> dict[str, str]:
    return {
        "code": code,
        "message": message,
    }


def make_result(
    status: str,
    template_key: str,
    image_name: str,
    layout_json: Any,
    errors: list[dict[str, str]],
    warnings: list[dict[str, str]],
) -> dict[str, Any]:
    return {
        "status": status,
        "layoutJson": layout_json,
        "source": build_source(template_key, image_name),
        "errors": errors,
        "warnings": warnings,
    }


def load_fixture(template_key: str) -> Any:
    fixture_name = TEMPLATE_FIXTURES[template_key]
    fixture_path = FIXTURE_DIR / fixture_name
    with fixture_path.open("r", encoding="utf-8") as file:
        return json.load(file)


def resolve_image_layout(template_key: str, image_name: str) -> dict[str, Any]:
    if template_key not in TEMPLATE_FIXTURES:
        return make_result(
            status="FAILED",
            template_key=template_key,
            image_name=image_name,
            layout_json=None,
            errors=[
                make_error(
                    "IMAGE_TEMPLATE_NOT_FOUND",
                    f"Unknown templateKey: {template_key}",
                )
            ],
            warnings=[],
        )

    try:
        layout_json = load_fixture(template_key)
    except FileNotFoundError:
        return make_result(
            status="FAILED",
            template_key=template_key,
            image_name=image_name,
            layout_json=None,
            errors=[
                make_error(
                    "IMAGE_TEMPLATE_LOAD_ERROR",
                    f"Fixture file not found for templateKey: {template_key}",
                )
            ],
            warnings=[],
        )
    except json.JSONDecodeError as exc:
        return make_result(
            status="FAILED",
            template_key=template_key,
            image_name=image_name,
            layout_json=None,
            errors=[
                make_error(
                    "IMAGE_TEMPLATE_LOAD_ERROR",
                    f"Fixture JSON parse failed at line {exc.lineno} column {exc.colno}",
                )
            ],
            warnings=[],
        )

    return make_result(
        status="SUCCESS",
        template_key=template_key,
        image_name=image_name,
        layout_json=layout_json,
        errors=[],
        warnings=[],
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Resolve image template fixtures to Layout JSON mock results."
    )
    parser.add_argument("template_key", help="Template key, for example: landing-basic")
    parser.add_argument("image_name", help="Image file name for source echo, for example: demo-home.png")
    return parser.parse_args()


def main() -> int:
    configure_output_encoding()
    args = parse_args()
    result = resolve_image_layout(args.template_key, args.image_name)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["status"] == "SUCCESS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
