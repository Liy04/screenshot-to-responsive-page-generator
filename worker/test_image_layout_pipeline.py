import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from worker.image_layout_pipeline import process_image_layout_job
from worker.layout_validator import validate_layout_document


PROJECT_ROOT = Path(__file__).resolve().parents[1]


class ImageLayoutPipelineTest(unittest.TestCase):
    def test_fallback_only_mode_returns_valid_layout_json(self):
        image_path = self.create_temp_image_file("landing-shot.png")
        try:
            result, exit_code = process_image_layout_job(
                job_id="job-fallback-only",
                image_path=image_path,
                mode="fallback-only",
                fallback=True,
            )
        finally:
            image_path.unlink(missing_ok=True)

        self.assertEqual(exit_code, 0)
        self.assertEqual(result["status"], "SUCCESS")
        self.assertTrue(result["fallbackUsed"])
        self.assertEqual(result["sourceType"], "FALLBACK_RULE")
        self.assertTrue(result["validation"]["ok"])
        self.assertIsInstance(result["layoutJson"], dict)
        self.assertTrue(result["previewHtml"])
        self.assert_preview_html_safe(result["previewHtml"])
        self.assertTrue(validate_layout_document(result["layoutJson"]).ok)

    def test_missing_image_path_returns_failed(self):
        result, exit_code = process_image_layout_job(
            job_id="job-missing-image",
            image_path="worker/fixtures/not-found.png",
            mode="fallback-only",
            fallback=True,
        )

        self.assertEqual(exit_code, 1)
        self.assertEqual(result["status"], "FAILED")
        self.assertFalse(result["validation"]["ok"])
        self.assertEqual(result["previewHtml"], "")
        self.assertIn("IMAGE_PATH_NOT_FOUND", {item["code"] for item in result["validation"]["errors"]})

    def test_real_ai_unavailable_uses_fallback_when_enabled(self):
        image_path = self.create_temp_image_file("dashboard-card.png")
        try:
            with patch(
                "worker.image_layout_pipeline.request_layout_intermediate",
                side_effect=RuntimeError("temporary ai outage"),
            ):
                result, exit_code = process_image_layout_job(
                    job_id="job-ai-fallback",
                    image_path=image_path,
                    mode="real-ai",
                    fallback=True,
                )
        finally:
            image_path.unlink(missing_ok=True)

        self.assertEqual(exit_code, 0)
        self.assertEqual(result["status"], "SUCCESS")
        self.assertTrue(result["fallbackUsed"])
        self.assertEqual(result["sourceType"], "FALLBACK_RULE")
        self.assertTrue(result["previewHtml"])
        self.assert_preview_html_safe(result["previewHtml"])
        self.assertIn("REAL_AI_UNAVAILABLE", {item["code"] for item in result["validation"]["warnings"]})
        self.assertTrue(validate_layout_document(result["layoutJson"]).ok)

    def test_real_ai_unavailable_fails_when_fallback_disabled(self):
        image_path = self.create_temp_image_file("landing-shot.png")
        try:
            with patch(
                "worker.image_layout_pipeline.request_layout_intermediate",
                side_effect=RuntimeError("temporary ai outage"),
            ):
                result, exit_code = process_image_layout_job(
                    job_id="job-ai-no-fallback",
                    image_path=image_path,
                    mode="real-ai",
                    fallback=False,
                )
        finally:
            image_path.unlink(missing_ok=True)

        self.assertEqual(exit_code, 1)
        self.assertEqual(result["status"], "FAILED")
        self.assertFalse(result["fallbackUsed"])
        self.assertEqual(result["layoutJson"], None)
        self.assertEqual(result["previewHtml"], "")
        self.assertIn("REAL_AI_GENERATION_FAILED", {item["code"] for item in result["validation"]["errors"]})

    def test_real_ai_success_returns_valid_layout_without_fallback(self):
        image_path = self.create_temp_image_file("auth-screen.png")
        ai_payload = {
            "pageName": "Auth Screen",
            "pageType": "auth",
            "sections": [
                {
                    "role": "content",
                    "elements": [
                        {"type": "text", "role": "heading", "content": "Sign in"},
                        {"type": "button", "role": "primaryAction", "content": "Continue"},
                    ],
                }
            ],
        }
        try:
            with patch("worker.image_layout_pipeline.request_layout_intermediate", return_value=ai_payload):
                result, exit_code = process_image_layout_job(
                    job_id="job-ai-success",
                    image_path=image_path,
                    mode="real-ai",
                    fallback=True,
                )
        finally:
            image_path.unlink(missing_ok=True)

        self.assertEqual(exit_code, 0)
        self.assertEqual(result["status"], "SUCCESS")
        self.assertFalse(result["fallbackUsed"])
        self.assertEqual(result["sourceType"], "REAL_AI")
        self.assertTrue(result["validation"]["ok"])
        self.assertTrue(result["previewHtml"])
        self.assert_preview_html_safe(result["previewHtml"])
        self.assertTrue(validate_layout_document(result["layoutJson"]).ok)

    def test_invalid_ai_layout_falls_back_to_valid_fixture(self):
        image_path = self.create_temp_image_file("card-list-reference.png")
        invalid_layout = {"page": {"name": "Broken"}}
        try:
            with patch("worker.image_layout_pipeline.request_layout_intermediate", return_value={"pageName": "Broken"}):
                with patch("worker.image_layout_pipeline.map_intermediate_to_layout_json", return_value=invalid_layout):
                    result, exit_code = process_image_layout_job(
                        job_id="job-ai-invalid-layout",
                        image_path=image_path,
                        mode="real-ai",
                        fallback=True,
                    )
        finally:
            image_path.unlink(missing_ok=True)

        self.assertEqual(exit_code, 0)
        self.assertEqual(result["status"], "SUCCESS")
        self.assertTrue(result["fallbackUsed"])
        self.assertEqual(result["sourceType"], "FALLBACK_RULE")
        self.assertTrue(result["validation"]["ok"])
        self.assertTrue(result["previewHtml"])
        self.assert_preview_html_safe(result["previewHtml"])
        self.assertTrue(validate_layout_document(result["layoutJson"]).ok)
        self.assertIn("AI_LAYOUT_INVALID", {item["code"] for item in result["validation"]["warnings"]})

    def test_result_does_not_expose_absolute_image_path(self):
        image_path = self.create_temp_image_file("landing-shot.png")
        try:
            result, _ = process_image_layout_job(
                job_id="job-no-abs-path",
                image_path=image_path,
                mode="fallback-only",
                fallback=True,
            )
        finally:
            image_path.unlink(missing_ok=True)

        serialized = json.dumps(result, ensure_ascii=False)
        self.assertNotIn(str(image_path), serialized)

    def assert_preview_html_safe(self, preview_html: str) -> None:
        lowered = preview_html.lower()
        self.assertNotIn("<script", lowered)
        self.assertNotIn("onclick=", lowered)
        self.assertNotIn("onload=", lowered)
        self.assertNotIn("onerror=", lowered)
        self.assertNotIn("<iframe", lowered)
        self.assertNotIn("<object", lowered)
        self.assertNotIn("<embed", lowered)
        self.assertNotIn("javascript:", lowered)

    def create_temp_image_file(self, name: str) -> Path:
        temp_file = tempfile.NamedTemporaryFile(
            mode="wb",
            suffix=Path(name).suffix,
            prefix=Path(name).stem + "-",
            dir=PROJECT_ROOT / "worker",
            delete=False,
        )
        temp_path = Path(temp_file.name)
        with temp_file:
            temp_file.write(b"\x89PNG\r\n\x1a\nmock-image-data")
        return temp_path


if __name__ == "__main__":
    unittest.main()
