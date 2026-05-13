import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from worker.real_ai_layout_client import (
    RealAIResponseError,
    RealAIUnavailableError,
    build_openai_client,
    extract_chat_completion_text,
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

    def test_parse_json_payload_rejects_non_json_text(self):
        with self.assertRaises(RealAIResponseError):
            parse_json_payload("not-json-response")

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

    def create_temp_image_file(self, suffix: str) -> Path:
        temp_file = tempfile.NamedTemporaryFile(mode="wb", suffix=suffix, delete=False)
        temp_path = Path(temp_file.name)
        with temp_file:
            temp_file.write(b"\x89PNG\r\n\x1a\nmock-image-data")
        return temp_path


if __name__ == "__main__":
    unittest.main()
