import copy
import json
import tempfile
import unittest
from pathlib import Path

from worker.layout_static_generator import generate_artifact
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
            "fontSize": "16px",
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
