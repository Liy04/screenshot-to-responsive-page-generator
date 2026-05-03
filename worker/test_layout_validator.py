import copy
import unittest
from pathlib import Path

from worker.layout_validator import load_json_file, validate_layout_document


PROJECT_ROOT = Path(__file__).resolve().parents[1]
VALID_EXAMPLES = PROJECT_ROOT / "examples" / "valid"
INVALID_EXAMPLES = PROJECT_ROOT / "examples" / "invalid"


class LayoutValidatorTest(unittest.TestCase):
    def test_valid_examples_pass(self):
        for path in sorted(VALID_EXAMPLES.glob("*.layout.json")):
            with self.subTest(path=path.name):
                result = validate_layout_document(load_json_file(path))

                self.assertTrue(result.ok, result.errors)

    def test_missing_version_fails_schema_validation(self):
        result = validate_layout_document(
            load_json_file(INVALID_EXAMPLES / "invalid-missing-version.layout.json")
        )

        self.assert_error_code(result, "SCHEMA_VALIDATION_ERROR")

    def test_duplicate_node_id_fails_business_validation(self):
        result = validate_layout_document(
            load_json_file(INVALID_EXAMPLES / "invalid-duplicate-node-id.layout.json")
        )

        self.assert_error_code(result, "DUPLICATE_NODE_ID")

    def test_responsive_target_fails_business_validation(self):
        result = validate_layout_document(
            load_json_file(INVALID_EXAMPLES / "invalid-responsive-target.layout.json")
        )

        self.assert_error_code(result, "RESPONSIVE_TARGET_NOT_FOUND")

    def test_text_without_content_fails_business_validation(self):
        document = load_json_file(VALID_EXAMPLES / "landing-page.layout.json")
        text_node = document["layout"]["children"][0]["children"][0]["children"][0]
        text_node.pop("content")

        result = validate_layout_document(document)

        self.assert_error_code(result, "TEXT_CONTENT_MISSING")

    def test_button_without_content_fails_business_validation(self):
        document = load_json_file(VALID_EXAMPLES / "landing-page.layout.json")
        button_node = document["layout"]["children"][0]["children"][0]["children"][1]
        button_node.pop("content")

        result = validate_layout_document(document)

        self.assert_error_code(result, "BUTTON_CONTENT_MISSING")

    def test_invalid_node_type_fails_schema_validation(self):
        document = copy.deepcopy(load_json_file(VALID_EXAMPLES / "landing-page.layout.json"))
        document["layout"]["children"][0]["type"] = "carousel"

        result = validate_layout_document(document)

        self.assert_error_code(result, "SCHEMA_VALIDATION_ERROR")

    def assert_error_code(self, result, code):
        self.assertFalse(result.ok)
        self.assertIn(code, {error.code for error in result.errors})


if __name__ == "__main__":
    unittest.main()
