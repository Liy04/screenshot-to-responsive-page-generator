import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from worker.real_ai_layout_client import (
    PROMPT_VERSION,
    RealAIResponseError,
    RealAIUnavailableError,
    build_prompt,
    build_openai_client,
    extract_chat_completion_text,
    get_configured_model,
    parse_json_payload,
    request_layout_intermediate,
)


class RealAILayoutClientTest(unittest.TestCase):
    def test_build_openai_client_uses_base_url_when_present(self):
        with patch("worker.real_ai_layout_client.OpenAI") as openai_class:
            with patch.dict(
                "os.environ",
                {
                    "OPENAI_API_KEY": "test-key",
                    "OPENAI_BASE_URL": "https://api.siliconflow.cn/v1",
                },
                clear=False,
            ):
                build_openai_client()

        openai_class.assert_called_once_with(
            api_key="test-key",
            base_url="https://api.siliconflow.cn/v1",
        )

    def test_missing_api_key_raises_unavailable_error(self):
        with patch.dict("os.environ", {}, clear=True):
            with self.assertRaises(RealAIUnavailableError):
                build_openai_client()

    def test_get_configured_model_uses_default_without_env_override(self):
        with patch.dict("os.environ", {}, clear=True):
            self.assertEqual(get_configured_model(), "gpt-4.1-mini")

    def test_get_configured_model_uses_env_override(self):
        with patch.dict("os.environ", {"OPENAI_MODEL": "Qwen/Qwen3-VL-32B-Instruct"}, clear=False):
            self.assertEqual(get_configured_model(), "Qwen/Qwen3-VL-32B-Instruct")

    def test_parse_json_payload_rejects_non_json_text(self):
        with self.assertRaises(RealAIResponseError):
            parse_json_payload("not-json-response")

    def test_parse_json_payload_accepts_plain_json(self):
        payload = parse_json_payload('{"pageName":"Demo","pageType":"marketing","sections":[]}')

        self.assertEqual(payload["pageName"], "Demo")

    def test_parse_json_payload_accepts_json_code_fence(self):
        payload = parse_json_payload(
            '```json\n{"pageName":"Demo","pageType":"marketing","sections":[]}\n```'
        )

        self.assertEqual(payload["pageType"], "marketing")

    def test_parse_json_payload_accepts_plain_code_fence(self):
        payload = parse_json_payload(
            '```\n{"pageName":"Demo","pageType":"marketing","sections":[]}\n```'
        )

        self.assertEqual(payload["pageType"], "marketing")

    def test_parse_json_payload_extracts_json_with_surrounding_text(self):
        payload = parse_json_payload(
            'Here is the extracted result:\n{"pageName":"Demo","pageType":"marketing","sections":[]}\nUse it carefully.'
        )

        self.assertEqual(payload["pageName"], "Demo")

    def test_extract_chat_completion_text_from_string_content(self):
        response = SimpleNamespace(
            choices=[SimpleNamespace(message=SimpleNamespace(content='{"pageName":"Demo"}'))]
        )

        text = extract_chat_completion_text(response)

        self.assertEqual(text, '{"pageName":"Demo"}')

    def test_request_layout_intermediate_parses_chat_completion_json(self):
        mock_client = SimpleNamespace(
            chat=SimpleNamespace(
                completions=SimpleNamespace(
                    create=lambda **_: SimpleNamespace(
                        choices=[
                            SimpleNamespace(
                                message=SimpleNamespace(
                                    content='{"pageName":"Demo","pageType":"marketing","sections":[]}'
                                )
                            )
                        ]
                    )
                )
            )
        )
        image_path = self.create_temp_image_file(".png")
        try:
            with patch("worker.real_ai_layout_client.build_openai_client", return_value=mock_client):
                with patch.dict("os.environ", {"OPENAI_MODEL": "Qwen/Qwen3-VL-32B-Instruct"}, clear=False):
                    payload = request_layout_intermediate(image_path, "job-ai-test")
        finally:
            image_path.unlink(missing_ok=True)

        self.assertEqual(payload["pageName"], "Demo")
        self.assertEqual(payload["pageType"], "marketing")
        self.assertEqual(PROMPT_VERSION, "week12-v1")

    def test_build_prompt_week12_v1_enforces_stable_visual_inventory_shape(self):
        prompt = build_prompt("job-ai-test", "sample.png")

        self.assertIn("Prompt version: week12-v1", prompt)
        self.assertIn("Return JSON only", prompt)
        self.assertIn("Do not return markdown, prose, HTML, CSS, or code fences.", prompt)
        self.assertIn("Never output a complete HTML page", prompt)
        self.assertIn("Return exactly one JSON object", prompt)
        self.assertIn("Allowed top-level keys in this exact order: pageName, pageType, texts, regions", prompt)
        self.assertIn("Do not include extra top-level keys", prompt)
        self.assertIn("Do not include metadata keys such as jobId, imageName", prompt)
        self.assertIn("OCR plus coarse structure", prompt)
        self.assertIn('"regions"', prompt)
        self.assertIn('"texts"', prompt)
        self.assertIn('"components"', prompt)
        self.assertIn("at least 8 visible texts", prompt)
        self.assertIn("metric cards", prompt)
        self.assertIn("pageName must come from visible screenshot text", prompt)
        self.assertNotIn("Job ID:", prompt)
        self.assertNotIn("Image name:", prompt)
        self.assertNotIn("job-ai-test", prompt)
        self.assertNotIn("sample.png", prompt)
        self.assertIn("Do not include style unless", prompt)

    def test_parse_json_payload_repairs_common_quoted_object_fragment(self):
        payload = parse_json_payload(
            '{"pageName":"Dashboard overview","regions":[{"role":"hero","texts":["Dashboard overview"]},"{"role":"metrics","texts":["Items","128"]}]}'
        )

        self.assertEqual(payload["pageName"], "Dashboard overview")
        self.assertEqual(payload["regions"][1]["role"], "metrics")

    def test_request_layout_intermediate_raises_for_non_json_model_output(self):
        mock_client = SimpleNamespace(
            chat=SimpleNamespace(
                completions=SimpleNamespace(
                    create=lambda **_: SimpleNamespace(
                        choices=[SimpleNamespace(message=SimpleNamespace(content="plain text output"))]
                    )
                )
            )
        )
        image_path = self.create_temp_image_file(".png")
        try:
            with patch("worker.real_ai_layout_client.build_openai_client", return_value=mock_client):
                with self.assertRaises(RealAIResponseError):
                    request_layout_intermediate(image_path, "job-ai-test")
        finally:
            image_path.unlink(missing_ok=True)

    def test_request_layout_intermediate_uses_bounded_generation_settings(self):
        captured_kwargs = {}

        def create_completion(**kwargs):
            captured_kwargs.update(kwargs)
            return SimpleNamespace(
                choices=[
                    SimpleNamespace(
                        message=SimpleNamespace(
                            content='{"pageName":"Demo","pageType":"marketing","sections":[]}'
                        )
                    )
                ]
            )

        mock_client = SimpleNamespace(
            chat=SimpleNamespace(completions=SimpleNamespace(create=create_completion))
        )
        image_path = self.create_temp_image_file(".png")
        try:
            with patch("worker.real_ai_layout_client.build_openai_client", return_value=mock_client):
                request_layout_intermediate(image_path, "job-ai-test")
        finally:
            image_path.unlink(missing_ok=True)

        self.assertEqual(captured_kwargs["temperature"], 0.0)
        self.assertEqual(captured_kwargs["max_tokens"], 1200)

    def create_temp_image_file(self, suffix: str) -> Path:
        temp_file = tempfile.NamedTemporaryFile(mode="wb", suffix=suffix, delete=False)
        temp_path = Path(temp_file.name)
        with temp_file:
            temp_file.write(b"\x89PNG\r\n\x1a\nmock-image-data")
        return temp_path


if __name__ == "__main__":
    unittest.main()
