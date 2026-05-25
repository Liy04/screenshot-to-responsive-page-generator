import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from worker.image_layout_pipeline import (
    map_intermediate_to_layout_json,
    process_image_layout_job,
    repair_intermediate_payload,
    repair_layout_json,
)
from worker.layout_validator import validate_layout_document
from worker.real_ai_layout_client import PROMPT_VERSION, RealAIResponseError


PROJECT_ROOT = Path(__file__).resolve().parents[1]


class ImageLayoutPipelineTest(unittest.TestCase):
    def test_repair_intermediate_payload_stabilizes_visual_inventory_shape(self):
        intermediate = {
            "pageName": "  Dashboard Overview  ",
            "pageType": "  DASHBOARD  ",
            "jobId": "job-raw",
            "imageName": "raw.png",
            "texts": [" Dashboard Overview ", "", "Items", "items", "128", "128"],
            "regions": [
                {
                    "role": "  Metrics ",
                    "texts": [" Items ", "128", "items", ""],
                    "components": [
                        {"type": "button", "role": "primary-action", "content": " Refresh "},
                        {"type": "button", "role": "primary-action", "content": " "},
                        " Quick Filter ",
                    ],
                },
                {
                    "role": "",
                    "texts": "not-a-list",
                    "components": ["   "],
                },
            ],
            "debugInfo": {"source": "model"},
        }

        repaired, used = repair_intermediate_payload(intermediate, "dashboard-page.png")

        self.assertTrue(used)
        self.assertEqual(list(repaired.keys())[:4], ["pageName", "pageType", "texts", "regions"])
        self.assertEqual(repaired["pageName"], "Dashboard Overview")
        self.assertEqual(repaired["pageType"], "dashboard")
        self.assertEqual(repaired["texts"], ["Dashboard Overview", "Items", "128"])
        self.assertEqual(len(repaired["regions"]), 1)
        self.assertEqual(repaired["regions"][0]["role"], "metrics")
        self.assertEqual(repaired["regions"][0]["texts"], ["Items", "128"])
        self.assertEqual(repaired["regions"][0]["components"][0], {"type": "button", "role": "primary-action", "content": "Refresh"})
        self.assertEqual(repaired["regions"][0]["components"][1], {"type": "text", "role": "body", "content": "Quick Filter"})
        self.assertNotIn("jobId", repaired)
        self.assertNotIn("imageName", repaired)
        self.assertNotIn("debugInfo", repaired)

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
        self.assertIsNone(result["fallbackReason"])
        self.assertEqual(result["sourceType"], "FALLBACK_RULE")
        self.assertEqual(result["promptVersion"], PROMPT_VERSION)
        self.assert_result_metadata(result, expected_model=None)
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
        self.assertEqual(result["fallbackReason"], "IMAGE_READ_FAILED")
        self.assert_result_metadata(result, expected_model=None)
        self.assertIn("IMAGE_PATH_NOT_FOUND", {item["code"] for item in result["validation"]["errors"]})

    def test_real_ai_unavailable_uses_fallback_when_enabled(self):
        image_path = self.create_temp_image_file("dashboard-card.png")
        try:
            with patch.dict("os.environ", {"OPENAI_MODEL": "metadata-model-fallback"}, clear=False):
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
        self.assertEqual(result["fallbackReason"], "MODEL_UNAVAILABLE")
        self.assertEqual(result["sourceType"], "FALLBACK_RULE")
        self.assertEqual(result["promptVersion"], PROMPT_VERSION)
        self.assert_result_metadata(result, expected_model="metadata-model-fallback")
        self.assertTrue(result["previewHtml"])
        self.assert_preview_html_safe(result["previewHtml"])
        self.assertIn("REAL_AI_UNAVAILABLE", {item["code"] for item in result["validation"]["warnings"]})
        self.assertTrue(validate_layout_document(result["layoutJson"]).ok)

    def test_real_ai_unavailable_fails_when_fallback_disabled(self):
        image_path = self.create_temp_image_file("landing-shot.png")
        try:
            with patch.dict("os.environ", {"OPENAI_MODEL": "metadata-model-failed"}, clear=False):
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
        self.assertEqual(result["fallbackReason"], "MODEL_UNAVAILABLE")
        self.assertEqual(result["layoutJson"], None)
        self.assertEqual(result["previewHtml"], "")
        self.assert_result_metadata(result, expected_model="metadata-model-failed")
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
            with patch.dict("os.environ", {"OPENAI_MODEL": "metadata-model-success"}, clear=False):
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
        self.assertIsNone(result["fallbackReason"])
        self.assertEqual(result["sourceType"], "REAL_AI")
        self.assertEqual(result["promptVersion"], PROMPT_VERSION)
        self.assert_result_metadata(result, expected_model="metadata-model-success")
        self.assertTrue(result["validation"]["ok"])
        self.assertTrue(result["previewHtml"])
        self.assert_preview_html_safe(result["previewHtml"])
        self.assertTrue(validate_layout_document(result["layoutJson"]).ok)

    def test_real_ai_mapping_adds_default_styles_and_sanitizes_intermediate_styles(self):
        image_path = self.create_temp_image_file("styled-card.png")
        ai_payload = {
            "pageName": "Styled Card",
            "pageType": "marketing",
            "sections": [
                {
                    "role": "cards",
                    "style": {
                        "backgroundColor": "#f8fafc",
                        "unknownSectionStyle": "ignored",
                    },
                    "elements": [
                        {
                            "type": "text",
                            "role": "heading",
                            "content": "Clean heading",
                            "style": {
                                "fontSize": "32px",
                                "color": "#111827",
                                "backgroundColor": "url(https://example.test/bad.png)",
                            },
                        },
                        {
                            "type": "button",
                            "role": "primary-action",
                            "content": "Start",
                            "style": {
                                "borderRadius": "999px",
                                "mystery": "ignored",
                                "color": "javascript:alert(1)",
                            },
                        },
                    ],
                }
            ],
        }
        try:
            with patch("worker.image_layout_pipeline.request_layout_intermediate", return_value=ai_payload):
                result, exit_code = process_image_layout_job(
                    job_id="job-ai-style-sanitize",
                    image_path=image_path,
                    mode="real-ai",
                    fallback=True,
                )
        finally:
            image_path.unlink(missing_ok=True)

        self.assertEqual(exit_code, 0)
        self.assertEqual(result["status"], "SUCCESS")
        self.assertFalse(result["fallbackUsed"])
        self.assertTrue(validate_layout_document(result["layoutJson"]).ok)

        section = result["layoutJson"]["layout"]["children"][0]
        heading = section["children"][0]
        button = section["children"][1]
        self.assertEqual(section["style"]["backgroundColor"], "#f8fafc")
        self.assertEqual(heading["style"]["fontSize"], "32px")
        self.assertEqual(heading["style"]["color"], "#111827")
        self.assertNotIn("url(", json.dumps(heading["style"]).lower())
        self.assertEqual(button["style"]["borderRadius"], "999px")
        self.assertEqual(button["style"]["backgroundColor"], "#2563eb")
        serialized_style = json.dumps(button["style"], ensure_ascii=False).lower()
        self.assertNotIn("javascript:", serialized_style)
        self.assertNotIn("mystery", serialized_style)

        layout_warning_messages = [item["message"] for item in result["layoutJson"]["warnings"]]
        self.assertTrue(any("Unsupported style key" in message for message in layout_warning_messages))
        self.assertTrue(any("Unsafe style value" in message for message in layout_warning_messages))

    def test_real_ai_mapping_keeps_nested_sections_and_element_children(self):
        image_path = self.create_temp_image_file("nested-card-page.png")
        ai_payload = {
            "pageName": "Responsive card page",
            "pageType": "generic",
            "sections": [
                {
                    "role": "header",
                    "elements": [
                        {
                            "type": "container",
                            "role": "nav",
                            "elements": [
                                "Mock Page",
                                {"type": "button", "role": "nav", "content": "Overview"},
                                {"type": "button", "role": "primary-action", "content": "Action"},
                            ],
                        }
                    ],
                    "sections": [
                        {
                            "role": "hero",
                            "elements": [
                                {
                                    "type": "text",
                                    "role": "heading",
                                    "content": "Responsive card page",
                                },
                                {
                                    "type": "button",
                                    "role": "primary-action",
                                    "content": "Primary",
                                },
                            ],
                        },
                        {
                            "role": "cards",
                            "elements": [
                                {
                                    "type": "card",
                                    "role": "card",
                                    "elements": [
                                        {
                                            "type": "text",
                                            "role": "heading",
                                            "content": "Content block",
                                        }
                                    ],
                                }
                            ],
                        },
                    ],
                }
            ],
        }
        try:
            with patch("worker.image_layout_pipeline.request_layout_intermediate", return_value=ai_payload):
                result, exit_code = process_image_layout_job(
                    job_id="job-ai-nested-intermediate",
                    image_path=image_path,
                    mode="real-ai",
                    fallback=True,
                )
        finally:
            image_path.unlink(missing_ok=True)

        self.assertEqual(exit_code, 0)
        self.assertEqual(result["status"], "SUCCESS")
        self.assertFalse(result["fallbackUsed"])
        self.assertTrue(validate_layout_document(result["layoutJson"]).ok)

        serialized_layout = json.dumps(result["layoutJson"], ensure_ascii=False)
        self.assertIn("Mock Page", serialized_layout)
        self.assertIn("Overview", serialized_layout)
        self.assertIn("Action", serialized_layout)
        self.assertIn("Responsive card page", serialized_layout)
        self.assertIn("Primary", serialized_layout)
        self.assertIn("Content block", serialized_layout)
        self.assertEqual(len(result["layoutJson"]["layout"]["children"]), 3)

    def test_real_ai_mapping_converts_visual_inventory_regions_to_sections(self):
        image_path = self.create_temp_image_file("inventory-page.png")
        ai_payload = {
            "pageName": "Mock Page",
            "pageType": "marketing",
            "regions": [
                {
                    "role": "header",
                    "texts": ["Mock Page"],
                    "components": [
                        {"type": "button", "role": "nav", "content": "Overview"},
                        {"type": "button", "role": "nav", "content": "Cards"},
                    ],
                },
                {
                    "role": "cards",
                    "texts": ["Responsive card page"],
                    "components": [
                        {
                            "type": "card",
                            "role": "card",
                            "content": "Content block",
                            "items": ["Useful details"],
                        },
                        {"type": "button", "role": "primary-action", "content": "Primary"},
                    ],
                },
            ],
        }
        try:
            with patch("worker.image_layout_pipeline.request_layout_intermediate", return_value=ai_payload):
                result, exit_code = process_image_layout_job(
                    job_id="job-ai-visual-inventory",
                    image_path=image_path,
                    mode="real-ai",
                    fallback=True,
                )
        finally:
            image_path.unlink(missing_ok=True)

        self.assertEqual(exit_code, 0)
        self.assertEqual(result["status"], "SUCCESS")
        self.assertFalse(result["fallbackUsed"])
        self.assertTrue(validate_layout_document(result["layoutJson"]).ok)

        serialized_layout = json.dumps(result["layoutJson"], ensure_ascii=False)
        self.assertIn("Mock Page", serialized_layout)
        self.assertIn("Overview", serialized_layout)
        self.assertIn("Cards", serialized_layout)
        self.assertIn("Responsive card page", serialized_layout)
        self.assertIn("Content block", serialized_layout)
        self.assertIn("Useful details", serialized_layout)
        self.assertIn("Primary", serialized_layout)
        self.assertEqual(len(result["layoutJson"]["layout"]["children"]), 2)

    def test_real_ai_mapping_turns_metric_inventory_pairs_into_cards(self):
        image_path = self.create_temp_image_file("dashboard-inventory.png")
        ai_payload = {
            "pageName": "Dashboard overview",
            "pageType": "dashboard",
            "regions": [
                {
                    "role": "metrics",
                    "texts": ["Items", "128", "Tasks", "42", "Checks", "96%", "Rate", "7.4"],
                }
            ],
        }
        try:
            with patch("worker.image_layout_pipeline.request_layout_intermediate", return_value=ai_payload):
                result, exit_code = process_image_layout_job(
                    job_id="job-ai-metric-inventory",
                    image_path=image_path,
                    mode="real-ai",
                    fallback=True,
                )
        finally:
            image_path.unlink(missing_ok=True)

        self.assertEqual(exit_code, 0)
        self.assertEqual(result["status"], "SUCCESS")
        self.assertFalse(result["fallbackUsed"])
        self.assertTrue(validate_layout_document(result["layoutJson"]).ok)

        metrics_section = result["layoutJson"]["layout"]["children"][0]
        self.assertEqual(metrics_section["role"], "metrics")
        self.assertEqual(len(metrics_section["children"]), 4)
        serialized_layout = json.dumps(result["layoutJson"], ensure_ascii=False)
        self.assertIn("Items", serialized_layout)
        self.assertIn("128", serialized_layout)
        self.assertIn("Rate", serialized_layout)
        self.assertIn("7.4", serialized_layout)

    def test_real_ai_mapping_uses_top_level_text_inventory_when_regions_missing(self):
        image_path = self.create_temp_image_file("text-inventory.png")
        ai_payload = {
            "pageName": "Visible Page",
            "pageType": "generic",
            "texts": ["Visible Page", "Primary action", "Secondary action"],
        }
        try:
            with patch("worker.image_layout_pipeline.request_layout_intermediate", return_value=ai_payload):
                result, exit_code = process_image_layout_job(
                    job_id="job-ai-text-inventory",
                    image_path=image_path,
                    mode="real-ai",
                    fallback=True,
                )
        finally:
            image_path.unlink(missing_ok=True)

        self.assertEqual(exit_code, 0)
        self.assertEqual(result["status"], "SUCCESS")
        self.assertFalse(result["fallbackUsed"])
        serialized_layout = json.dumps(result["layoutJson"], ensure_ascii=False)
        self.assertIn("Visible Page", serialized_layout)
        self.assertIn("Primary action", serialized_layout)
        self.assertIn("Secondary action", serialized_layout)

    def test_real_ai_mapping_converts_form_inventory_to_semantic_nodes(self):
        image_path = self.create_temp_image_file("form-inventory.png")
        ai_payload = {
            "pageName": "Sign in",
            "pageType": "auth",
            "regions": [
                {
                    "role": "form",
                    "texts": ["Sign in"],
                    "components": [
                        {
                            "type": "form",
                            "role": "form",
                            "items": [
                                {"type": "input", "role": "email", "label": "Email"},
                                {"type": "input", "role": "password", "label": "Password"},
                                {"type": "button", "role": "primary-action", "content": "Continue"},
                            ],
                        }
                    ],
                }
            ],
        }
        try:
            with patch("worker.image_layout_pipeline.request_layout_intermediate", return_value=ai_payload):
                result, exit_code = process_image_layout_job(
                    job_id="job-ai-form-inventory",
                    image_path=image_path,
                    mode="real-ai",
                    fallback=True,
                )
        finally:
            image_path.unlink(missing_ok=True)

        self.assertEqual(exit_code, 0)
        self.assertEqual(result["status"], "SUCCESS")
        self.assertFalse(result["fallbackUsed"])
        self.assertTrue(validate_layout_document(result["layoutJson"]).ok)

        section_children = result["layoutJson"]["layout"]["children"][0]["children"]
        self.assertTrue(any(node["type"] == "form" for node in section_children))
        serialized_layout = json.dumps(result["layoutJson"], ensure_ascii=False)
        self.assertIn('"type": "input"', serialized_layout)
        self.assertIn('"type": "button"', serialized_layout)
        self.assertIn("Email", serialized_layout)
        self.assertIn("Password", serialized_layout)
        self.assertIn("Continue", serialized_layout)

    def test_repair_layout_json_adds_semantic_defaults_recursively(self):
        broken_layout = {
            "version": "0.1",
            "layout": {
                "id": "root",
                "type": "page",
                "children": [
                    {
                        "id": "section-1",
                        "type": "section",
                        "children": [
                            {
                                "id": "card-1",
                                "type": "card",
                                "children": [
                                    {
                                        "id": "title-1",
                                        "content": "Items",
                                        "style": {
                                            "positionHack": "absolute",
                                            "fontSize": "24px",
                                        },
                                    }
                                ],
                            }
                        ],
                    }
                ],
            },
        }

        repaired = repair_layout_json(broken_layout, "dashboard.png")
        section = repaired["layout"]["children"][0]
        card = section["children"][0]
        text = card["children"][0]

        self.assertEqual(section["role"], "section")
        self.assertEqual(card["role"], "card")
        self.assertEqual(text["type"], "text")
        self.assertEqual(text["role"], "body")
        self.assertNotIn("positionHack", text["style"])
        self.assertEqual(text["style"]["fontSize"], "24px")
        self.assertEqual(text["constraints"]["horizontal"], "fill")
        self.assertEqual(text["constraints"]["vertical"], "hug")

    def test_real_ai_mapping_uses_input_label_when_content_missing(self):
        image_path = self.create_temp_image_file("form-labels.png")
        ai_payload = {
            "pageName": "Request settings",
            "pageType": "form",
            "regions": [
                {
                    "role": "form",
                    "texts": ["Request settings"],
                    "components": [
                        {
                            "type": "form",
                            "role": "form",
                            "items": [
                                {"type": "input", "role": "text", "label": "Project label"},
                                {"type": "button", "role": "primary-action", "content": "Submit"},
                            ],
                        }
                    ],
                }
            ],
        }
        try:
            with patch("worker.image_layout_pipeline.request_layout_intermediate", return_value=ai_payload):
                result, exit_code = process_image_layout_job(
                    job_id="job-ai-form-labels",
                    image_path=image_path,
                    mode="real-ai",
                    fallback=True,
                )
        finally:
            image_path.unlink(missing_ok=True)

        self.assertEqual(exit_code, 0)
        self.assertEqual(result["status"], "SUCCESS")
        self.assertFalse(result["fallbackUsed"])

        form_node = next(
            node for node in result["layoutJson"]["layout"]["children"][0]["children"] if node["type"] == "form"
        )
        input_node = next(child for child in form_node["children"] if child["type"] == "input")
        self.assertEqual(input_node["content"], "Project label")
        self.assertIn("border", input_node["style"])
        self.assertIn("borderRadius", input_node["style"])

    def test_map_intermediate_metric_cards_apply_card_and_metric_styles(self):
        layout = map_intermediate_to_layout_json(
            {
                "pageName": "Dashboard overview",
                "pageType": "dashboard",
                "regions": [
                    {
                        "role": "metrics",
                        "texts": ["Items", "128", "Tasks", "42"],
                    }
                ],
            },
            "dashboard-cards-page.png",
        )

        metrics_section = layout["layout"]["children"][0]
        self.assertEqual(metrics_section["role"], "metrics")
        self.assertIn("display", metrics_section["style"])

        metric_card = metrics_section["children"][0]
        self.assertEqual(metric_card["type"], "card")
        self.assertEqual(metric_card["role"], "metric")
        self.assertIn("borderRadius", metric_card["style"])

        label_node = metric_card["children"][0]
        value_node = metric_card["children"][1]
        self.assertEqual(label_node["role"], "label")
        self.assertEqual(value_node["role"], "metric")
        self.assertEqual(label_node["content"], "Items")
        self.assertEqual(value_node["content"], "128")
        self.assertEqual(value_node["style"]["fontWeight"], "700")

    def test_repair_layout_json_infers_form_input_and_button_children(self):
        broken_layout = {
            "version": "0.1",
            "layout": {
                "id": "root",
                "type": "page",
                "children": [
                    {
                        "id": "form-1",
                        "type": "form",
                        "children": [
                            {"id": "field-1", "label": "Email"},
                            {"id": "action-1", "content": "Continue"},
                        ],
                    }
                ],
            },
        }

        repaired = repair_layout_json(broken_layout, "sign-in.png")
        form_node = repaired["layout"]["children"][0]
        input_node = form_node["children"][0]
        button_node = form_node["children"][1]

        self.assertEqual(form_node["type"], "form")
        self.assertEqual(input_node["type"], "input")
        self.assertEqual(input_node["content"], "Email")
        self.assertIn("border", input_node["style"])
        self.assertEqual(button_node["type"], "button")
        self.assertEqual(button_node["content"], "Continue")
        self.assertIn("backgroundColor", button_node["style"])

    def test_repair_layout_json_generates_stable_missing_node_ids(self):
        broken_layout = {
            "version": "0.1",
            "layout": {
                "type": "page",
                "children": [
                    {"content": "Stable text"},
                    {
                        "type": "form",
                        "children": [
                            {"label": "Email"},
                            {"content": "Continue"},
                        ],
                    },
                ],
            },
        }

        first = repair_layout_json(broken_layout, "stable-page.png")
        second = repair_layout_json(broken_layout, "stable-page.png")

        self.assertEqual(first["layout"]["id"], second["layout"]["id"])
        self.assertEqual(first["layout"]["children"][0]["id"], second["layout"]["children"][0]["id"])
        self.assertEqual(first["layout"]["children"][1]["children"][0]["id"], second["layout"]["children"][1]["children"][0]["id"])
        self.assertEqual(first["layout"]["id"], "repaired-page-layout")
        self.assertEqual(first["layout"]["children"][0]["id"], "repaired-text-layout-children-0")

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
        self.assertEqual(result["fallbackReason"], "SCHEMA_VALIDATION_FAILED")
        self.assertEqual(result["sourceType"], "FALLBACK_RULE")
        self.assertEqual(result["promptVersion"], PROMPT_VERSION)
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

    def test_result_metadata_does_not_expose_openai_api_key_value(self):
        image_path = self.create_temp_image_file("dashboard-card.png")
        secret_value = "sk-test-secret-value"
        try:
            with patch.dict(
                "os.environ",
                {
                    "OPENAI_API_KEY": secret_value,
                    "OPENAI_MODEL": "metadata-safe-model",
                },
                clear=False,
            ):
                with patch(
                    "worker.image_layout_pipeline.request_layout_intermediate",
                    side_effect=RuntimeError("temporary ai outage"),
                ):
                    result, exit_code = process_image_layout_job(
                        job_id="job-metadata-secret-check",
                        image_path=image_path,
                        mode="real-ai",
                        fallback=True,
                    )
        finally:
            image_path.unlink(missing_ok=True)

        self.assertEqual(exit_code, 0)
        self.assert_result_metadata(result, expected_model="metadata-safe-model")
        serialized = json.dumps(result, ensure_ascii=False)
        self.assertNotIn(secret_value, serialized)

    def test_real_ai_non_json_output_uses_fallback_without_crashing(self):
        image_path = self.create_temp_image_file("landing-shot.png")
        try:
            with patch(
                "worker.image_layout_pipeline.request_layout_intermediate",
                side_effect=RealAIResponseError("Model output did not contain valid JSON"),
            ):
                result, exit_code = process_image_layout_job(
                    job_id="job-ai-non-json-fallback",
                    image_path=image_path,
                    mode="real-ai",
                    fallback=True,
                )
        finally:
            image_path.unlink(missing_ok=True)

        self.assertEqual(exit_code, 0)
        self.assertEqual(result["status"], "SUCCESS")
        self.assertTrue(result["fallbackUsed"])
        self.assertEqual(result["fallbackReason"], "MODEL_NON_JSON_OUTPUT")
        self.assertEqual(result["promptVersion"], PROMPT_VERSION)
        self.assertTrue(result["previewHtml"])
        self.assertIn("REAL_AI_UNAVAILABLE", {item["code"] for item in result["validation"]["warnings"]})

    def test_real_ai_intermediate_repair_keeps_real_ai_path(self):
        image_path = self.create_temp_image_file("repair-me.png")
        ai_payload = {
            "sections": [
                {
                    "elements": [
                        {"type": "text", "role": "heading", "content": "Hello"},
                    ]
                }
            ]
        }
        try:
            with patch("worker.image_layout_pipeline.request_layout_intermediate", return_value=ai_payload):
                result, exit_code = process_image_layout_job(
                    job_id="job-ai-repair-success",
                    image_path=image_path,
                    mode="real-ai",
                    fallback=True,
                )
        finally:
            image_path.unlink(missing_ok=True)

        self.assertEqual(exit_code, 0)
        self.assertEqual(result["status"], "SUCCESS")
        self.assertFalse(result["fallbackUsed"])
        self.assertIsNone(result["fallbackReason"])
        self.assertEqual(result["sourceType"], "REAL_AI")
        self.assertIn("INTERMEDIATE_REPAIRED", {item["code"] for item in result["validation"]["warnings"]})
        self.assertTrue(validate_layout_document(result["layoutJson"]).ok)

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

    def assert_result_metadata(self, result: dict, expected_model: str | None) -> None:
        self.assertIn("durationMs", result)
        self.assertIsInstance(result["durationMs"], int)
        self.assertGreaterEqual(result["durationMs"], 0)
        self.assertIn("model", result)
        self.assertEqual(result["model"], expected_model)

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
