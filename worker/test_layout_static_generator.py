import copy
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from worker.layout_static_generator import compile_document, generate_artifact
from worker.layout_validator import load_json_file


PROJECT_ROOT = Path(__file__).resolve().parents[1]
VALID_EXAMPLES = PROJECT_ROOT / "examples" / "valid"
INVALID_EXAMPLES = PROJECT_ROOT / "examples" / "invalid"
REQUIRED_ARTIFACT_FIELDS = {
    "version",
    "artifactType",
    "jobId",
    "generator",
    "source",
    "validation",
    "status",
    "htmlCode",
    "cssCode",
    "vueCode",
    "unsupportedNodes",
    "createdAt",
}


class LayoutStaticGeneratorTest(unittest.TestCase):
    def test_valid_examples_generate_success_artifacts(self):
        for path in sorted(VALID_EXAMPLES.glob("*.layout.json")):
            with self.subTest(path=path.name):
                artifact, exit_code = generate_artifact(path)

                self.assertEqual(exit_code, 0)
                self.assertEqual(artifact["status"], "SUCCESS")
                self.assertEqual(artifact["artifactType"], "generated-page")
                self.assertEqual(artifact["generator"]["name"], "layout-static-generator")
                self.assertTrue(artifact["htmlCode"])
                self.assertTrue(artifact["cssCode"])
                self.assertEqual(artifact["validation"]["errors"], [])

    def test_invalid_examples_generate_failed_artifacts(self):
        for path in sorted(INVALID_EXAMPLES.glob("*.layout.json")):
            with self.subTest(path=path.name):
                artifact, exit_code = generate_artifact(path)

                self.assertEqual(exit_code, 1)
                self.assertEqual(artifact["status"], "FAILED")
                self.assertFalse(artifact["validation"]["passed"])
                self.assertTrue(artifact["validation"]["errors"])
                self.assertEqual(artifact["htmlCode"], "")
                self.assertEqual(artifact["cssCode"], "")
                self.assertEqual(artifact["vueCode"], "")

    def test_artifact_required_fields_exist(self):
        artifact, _ = generate_artifact(VALID_EXAMPLES / "landing-page.layout.json")

        self.assertTrue(REQUIRED_ARTIFACT_FIELDS.issubset(artifact.keys()))

    def test_success_artifact_sets_validation_passed_true(self):
        artifact, _ = generate_artifact(VALID_EXAMPLES / "landing-page.layout.json")

        self.assertTrue(artifact["validation"]["passed"])

    def test_layout_hash_is_stable(self):
        path = VALID_EXAMPLES / "landing-page.layout.json"

        first, _ = generate_artifact(path)
        second, _ = generate_artifact(path)

        self.assertEqual(first["source"]["layoutHash"], second["source"]["layoutHash"])

    def test_html_escapes_text_and_button_content(self):
        document = load_json_file(VALID_EXAMPLES / "landing-page.layout.json")
        text_node = document["layout"]["children"][0]["children"][0]["children"][0]
        button_node = document["layout"]["children"][0]["children"][0]["children"][1]
        text_node["content"] = '<script>alert("x")</script> & text'
        button_node["content"] = 'Click "now" & continue'

        artifact = self.generate_from_document(document)
        html_code = artifact["htmlCode"]

        self.assertEqual(artifact["status"], "SUCCESS")
        self.assertIn("&lt;script&gt;alert", html_code)
        self.assertIn("&amp; text", html_code)
        self.assertIn('Click "now" &amp; continue', html_code)
        self.assertNotIn("<script", html_code.lower())

    def test_html_excludes_inline_events_and_javascript_urls(self):
        document = self.document_with_safe_style_subset()
        image_node = document["layout"]["children"][0]["children"][1]
        image_node["src"] = "javascript:alert(1)"
        image_node["onclick"] = "alert(1)"
        document["layout"]["children"][0]["onload"] = "alert(1)"

        artifact = self.generate_from_document(document)
        html_code = artifact["htmlCode"].lower()

        self.assertEqual(artifact["status"], "SUCCESS")
        self.assertNotIn("onclick=", html_code)
        self.assertNotIn("onload=", html_code)
        self.assertNotIn("javascript:", html_code)

    def test_unknown_style_field_adds_warning(self):
        document = self.document_with_safe_style_subset()
        document["layout"]["style"]["unknownStyle"] = "quiet"

        artifact = self.generate_from_document(document)

        self.assert_warning_code(artifact, "UNKNOWN_STYLE_FIELD")

    def test_unsafe_css_value_is_skipped_and_warned(self):
        document = self.document_with_safe_style_subset()
        document["layout"]["style"]["backgroundColor"] = "url(javascript:alert(1))"

        artifact = self.generate_from_document(document)

        self.assert_warning_code(artifact, "UNSAFE_CSS_VALUE")
        self.assertNotIn("url(javascript", artifact["cssCode"])

    def test_width_and_height_are_compiled(self):
        document = self.document_with_safe_style_subset()
        document["layout"]["style"]["width"] = "320px"
        document["layout"]["style"]["height"] = "240px"

        artifact = self.generate_from_document(document)

        self.assertIn("width: 320px;", artifact["cssCode"])
        self.assertIn("height: 240px;", artifact["cssCode"])

    def test_justify_content_is_compiled(self):
        document = self.document_with_safe_style_subset()
        document["layout"]["style"]["justifyContent"] = "space-between"

        artifact = self.generate_from_document(document)

        self.assertIn("justify-content: space-between;", artifact["cssCode"])

    def test_align_items_is_compiled(self):
        document = self.document_with_safe_style_subset()
        document["layout"]["style"]["alignItems"] = "center"

        artifact = self.generate_from_document(document)

        self.assertIn("align-items: center;", artifact["cssCode"])

    def test_max_width_is_compiled(self):
        document = self.document_with_safe_style_subset()
        document["layout"]["style"]["maxWidth"] = "640px"

        artifact = self.generate_from_document(document)

        self.assertIn("max-width: 640px;", artifact["cssCode"])

    def test_line_height_is_compiled(self):
        document = self.document_with_safe_style_subset()
        text_node = document["layout"]["children"][0]["children"][0]["children"][0]
        text_node["style"]["lineHeight"] = "1.5"

        artifact = self.generate_from_document(document)

        self.assertIn("line-height: 1.5;", artifact["cssCode"])

    def test_text_align_is_compiled(self):
        document = self.document_with_safe_style_subset()
        text_node = document["layout"]["children"][0]["children"][0]["children"][0]
        text_node["style"]["textAlign"] = "center"

        artifact = self.generate_from_document(document)

        self.assertIn("text-align: center;", artifact["cssCode"])

    def test_object_fit_is_compiled_for_image(self):
        document = self.document_with_safe_style_subset()
        image_node = document["layout"]["children"][0]["children"][1]
        image_node["style"]["objectFit"] = "cover"

        artifact = self.generate_from_document(document)

        self.assertIn("object-fit: cover;", artifact["cssCode"])

    def test_unsafe_width_or_height_is_skipped_and_warned(self):
        document = self.document_with_safe_style_subset()
        document["layout"]["style"]["width"] = "calc(100% - 10px)"
        document["layout"]["style"]["height"] = "fit-content"

        artifact = self.generate_from_document(document)

        self.assert_warning_code(artifact, "UNSAFE_CSS_VALUE")
        self.assertNotIn("width: calc(100% - 10px);", artifact["cssCode"])
        self.assertNotIn("height: fit-content;", artifact["cssCode"])

    def test_unsafe_max_width_is_skipped_and_warned(self):
        document = self.document_with_safe_style_subset()
        document["layout"]["style"]["maxWidth"] = "min(100%, 500px)"

        artifact = self.generate_from_document(document)

        self.assert_warning_code(artifact, "UNSAFE_CSS_VALUE")
        self.assertNotIn("max-width: min(100%, 500px);", artifact["cssCode"])

    def test_unsafe_line_height_is_skipped_and_warned(self):
        document = self.document_with_safe_style_subset()
        text_node = document["layout"]["children"][0]["children"][0]["children"][0]
        text_node["style"]["lineHeight"] = "calc(1 + 2)"

        artifact = self.generate_from_document(document)

        self.assert_warning_code(artifact, "UNSAFE_CSS_VALUE")
        self.assertNotIn("line-height: calc(1 + 2);", artifact["cssCode"])

    def test_unsafe_text_align_is_skipped_and_warned(self):
        document = self.document_with_safe_style_subset()
        text_node = document["layout"]["children"][0]["children"][0]["children"][0]
        text_node["style"]["textAlign"] = "middle"

        artifact = self.generate_from_document(document)

        self.assert_warning_code(artifact, "UNSAFE_CSS_VALUE")
        self.assertNotIn("text-align: middle;", artifact["cssCode"])

    def test_unsafe_object_fit_is_skipped_and_warned(self):
        document = self.document_with_safe_style_subset()
        image_node = document["layout"]["children"][0]["children"][1]
        image_node["style"]["objectFit"] = "zoom"

        artifact = self.generate_from_document(document)

        self.assert_warning_code(artifact, "UNSAFE_CSS_VALUE")
        self.assertNotIn("object-fit: zoom;", artifact["cssCode"])

    def test_unsafe_image_src_is_skipped_and_warned(self):
        document = self.document_with_safe_style_subset()
        image_node = document["layout"]["children"][0]["children"][1]
        image_node["src"] = "data:image/svg+xml,<svg onload=alert(1)>"

        artifact = self.generate_from_document(document)

        self.assert_warning_code(artifact, "IMAGE_SAFE_SRC_MISSING")
        self.assertNotIn("data:image", artifact["htmlCode"])
        self.assertNotIn("onload", artifact["htmlCode"].lower())

    def test_failed_artifact_keeps_empty_code_fields(self):
        artifact, exit_code = generate_artifact(INVALID_EXAMPLES / "invalid-missing-version.layout.json")

        self.assertEqual(exit_code, 1)
        self.assertFalse(artifact["validation"]["passed"])
        self.assertEqual(artifact["htmlCode"], "")
        self.assertEqual(artifact["cssCode"], "")
        self.assertEqual(artifact["vueCode"], "")

    def test_unsupported_node_is_recorded_without_rendering_html(self):
        document = self.document_with_safe_style_subset()
        unsupported = {
            "id": "landing-unsupported-node",
            "type": "table",
            "role": "unsupported",
            "bounds": {"x": 0, "y": 0, "width": 100, "height": 40},
            "style": {},
            "constraints": {"horizontal": "fill", "vertical": "hug"},
            "interactions": [],
            "children": [],
        }
        document["layout"]["children"].append(unsupported)

        with patch("worker.layout_static_generator.node_mapping", wraps=__import__("worker.layout_static_generator", fromlist=["node_mapping"]).node_mapping):
            html_code, _, _, warnings, unsupported_nodes = compile_document(document)

        self.assertEqual(unsupported_nodes[0]["id"], "landing-unsupported-node")
        self.assertEqual(unsupported_nodes[0]["type"], "table")
        self.assertNotIn("landing-unsupported-node", html_code)
        self.assertIn("UNSUPPORTED_NODE_TYPE", {warning.code for warning in warnings})

    def generate_from_document(self, document):
        temp_file = tempfile.NamedTemporaryFile(
            mode="w",
            suffix=".layout.json",
            prefix="layout-static-generator-test-",
            dir=PROJECT_ROOT / "worker",
            delete=False,
            encoding="utf-8",
        )
        temp_path = Path(temp_file.name)
        try:
            with temp_file:
                temp_file.write(json.dumps(document, ensure_ascii=False))
            artifact, exit_code = generate_artifact(temp_path)
            self.assertEqual(exit_code, 0, artifact["validation"]["errors"])
            return artifact
        finally:
            if temp_path.exists():
                temp_path.unlink()

    def document_with_safe_style_subset(self):
        document = copy.deepcopy(load_json_file(VALID_EXAMPLES / "landing-page.layout.json"))
        self.replace_styles(document["layout"])
        image_node = document["layout"]["children"][0]["children"][1]
        image_node["src"] = "https://example.com/image.png"
        return document

    def replace_styles(self, node):
        node["style"] = {
            "backgroundColor": "#ffffff",
            "color": "#111827",
            "width": "100%",
            "height": "240px",
            "maxWidth": "960px",
            "fontSize": "16px",
            "lineHeight": "1.4",
            "fontWeight": "bold",
            "borderRadius": "8px",
            "padding": "16px",
            "margin": "0px",
            "textAlign": "left",
            "display": "flex",
            "flexDirection": "column",
            "gap": "12px",
            "objectFit": "contain",
            "justifyContent": "center",
            "alignItems": "stretch",
        }
        for child in node.get("children", []):
            self.replace_styles(child)

    def assert_warning_code(self, artifact, code):
        warning_codes = {warning["code"] for warning in artifact["validation"]["warnings"]}
        self.assertIn(code, warning_codes)


if __name__ == "__main__":
    unittest.main()
