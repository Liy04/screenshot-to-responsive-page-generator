import copy
import unittest

from worker.image_layout_resolver import resolve_image_layout
from worker.layout_validator import validate_layout_document


class ImageLayoutResolverTest(unittest.TestCase):
    def test_landing_basic_returns_success(self):
        result = resolve_image_layout("landing-basic", "demo-home.png")

        self.assertEqual(result["status"], "SUCCESS")
        self.assertEqual(result["errors"], [])
        self.assertEqual(result["warnings"], [])
        self.assertIsInstance(result["layoutJson"], dict)

    def test_card_list_returns_success(self):
        result = resolve_image_layout("card-list", "demo-list.png")

        self.assertEqual(result["status"], "SUCCESS")
        self.assertEqual(result["errors"], [])
        self.assertEqual(result["warnings"], [])
        self.assertIsInstance(result["layoutJson"], dict)

    def test_unknown_template_returns_failed(self):
        result = resolve_image_layout("unknown-template", "demo.png")

        self.assertEqual(result["status"], "FAILED")
        self.assertIsNone(result["layoutJson"])
        self.assertTrue(result["errors"])

    def test_unknown_template_contains_not_found_error_code(self):
        result = resolve_image_layout("unknown-template", "demo.png")

        self.assertEqual(result["errors"][0]["code"], "IMAGE_TEMPLATE_NOT_FOUND")

    def test_source_type_is_image_template_mock(self):
        result = resolve_image_layout("landing-basic", "demo-home.png")

        self.assertEqual(result["source"]["type"], "IMAGE_TEMPLATE_MOCK")

    def test_source_template_key_matches_input(self):
        result = resolve_image_layout("card-list", "demo-list.png")

        self.assertEqual(result["source"]["templateKey"], "card-list")
        self.assertEqual(result["source"]["imageName"], "demo-list.png")

    def test_landing_basic_layout_passes_validator(self):
        result = resolve_image_layout("landing-basic", "demo-home.png")

        validation = validate_layout_document(copy.deepcopy(result["layoutJson"]))

        self.assertTrue(validation.ok, validation.errors)

    def test_card_list_layout_passes_validator(self):
        result = resolve_image_layout("card-list", "demo-list.png")

        validation = validate_layout_document(copy.deepcopy(result["layoutJson"]))

        self.assertTrue(validation.ok, validation.errors)

    def test_invalid_layout_fails_validator(self):
        result = resolve_image_layout("invalid-layout", "demo-invalid.png")

        validation = validate_layout_document(copy.deepcopy(result["layoutJson"]))

        self.assertFalse(validation.ok)
        self.assertIn("SCHEMA_VALIDATION_ERROR", {error.code for error in validation.errors})

    def test_same_template_resolution_is_stable(self):
        first = resolve_image_layout("landing-basic", "demo-home.png")
        second = resolve_image_layout("landing-basic", "demo-home.png")

        self.assertEqual(first, second)


if __name__ == "__main__":
    unittest.main()
