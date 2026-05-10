package com.screenshot.generator.backend.layout;

import java.util.List;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.ConcurrentMap;
import java.util.concurrent.atomic.AtomicLong;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.node.ArrayNode;
import com.fasterxml.jackson.databind.node.ObjectNode;
import com.screenshot.generator.backend.common.ResourceNotFoundException;

import org.springframework.stereotype.Service;

@Service
public class ImagePageJobService {

    private static final String SOURCE_TYPE = "IMAGE_TEMPLATE_MOCK";
    private static final int MAX_IMAGE_NAME_LENGTH = 255;

    private final ObjectMapper objectMapper;
    private final AtomicLong jobSequence = new AtomicLong(1);
    private final ConcurrentMap<String, ImagePageJobResponse> jobs = new ConcurrentHashMap<>();

    public ImagePageJobService(ObjectMapper objectMapper) {
        this.objectMapper = objectMapper;
    }

    public ImagePageJobResponse createJob(JsonNode requestJson) {
        ImagePageJobRequest request = parseRequest(requestJson);
        String imageName = normalizeImageName(request.imageName());
        String templateKey = normalizeTemplateKey(request.templateKey());

        ImagePageJobResponse job = createJobResponse(nextJobId(), imageName, templateKey);
        jobs.put(job.jobId(), job);
        return job;
    }

    public ImagePageJobResponse getJob(String jobId) {
        ImagePageJobResponse job = jobs.get(jobId);
        if (job == null) {
            throw new ResourceNotFoundException("image-page job 不存在");
        }
        return job;
    }

    private ImagePageJobRequest parseRequest(JsonNode requestJson) {
        if (requestJson == null || requestJson.isNull()) {
            throw new IllegalArgumentException("请求体不能为空");
        }

        if (!requestJson.isObject()) {
            throw new IllegalArgumentException("请求体必须是 JSON 对象");
        }

        try {
            return objectMapper.treeToValue(requestJson, ImagePageJobRequest.class);
        } catch (JsonProcessingException exception) {
            throw new IllegalArgumentException("请求体格式不合法");
        }
    }

    private String normalizeImageName(String imageName) {
        if (imageName == null || imageName.isBlank()) {
            throw new IllegalArgumentException("imageName 不能为空");
        }

        String normalized = imageName.trim();
        if (normalized.length() > MAX_IMAGE_NAME_LENGTH) {
            throw new IllegalArgumentException("imageName 不能超过 255 个字符");
        }
        return normalized;
    }

    private String normalizeTemplateKey(String templateKey) {
        if (templateKey == null || templateKey.isBlank()) {
            throw new IllegalArgumentException("templateKey 不能为空");
        }

        String normalized = templateKey.trim();
        if (!isSupportedTemplate(normalized)) {
            throw new IllegalArgumentException("Unknown templateKey: " + normalized);
        }
        return normalized;
    }

    private boolean isSupportedTemplate(String templateKey) {
        return "landing-basic".equals(templateKey)
                || "card-list".equals(templateKey)
                || "invalid-layout".equals(templateKey);
    }

    private ImagePageJobResponse createJobResponse(String jobId, String imageName, String templateKey) {
        if ("invalid-layout".equals(templateKey)) {
            List<ImageLayoutIssue> errors = List.of(new ImageLayoutIssue(
                    "INVALID_LAYOUT_TEMPLATE",
                    "invalid-layout 是用于 image-page 失败状态展示的已知 mock 模板",
                    "layout"));
            return new ImagePageJobResponse(
                    jobId,
                    "FAILED",
                    SOURCE_TYPE,
                    imageName,
                    templateKey,
                    new ImageLayoutArtifact("FAILED", invalidLayoutJson(imageName, templateKey)),
                    null,
                    errors,
                    List.of());
        }

        return new ImagePageJobResponse(
                jobId,
                "SUCCESS",
                SOURCE_TYPE,
                imageName,
                templateKey,
                new ImageLayoutArtifact("SUCCESS", successLayoutJson(imageName, templateKey)),
                successGeneratedPageArtifact(templateKey),
                List.of(),
                List.of());
    }

    private String nextJobId() {
        return "img-page-" + String.format("%03d", jobSequence.getAndIncrement());
    }

    private ObjectNode successLayoutJson(String imageName, String templateKey) {
        ObjectNode root = baseLayoutJson(imageName, templateKey);
        root.set("layout", layoutNode(templateKey));
        return root;
    }

    private ObjectNode invalidLayoutJson(String imageName, String templateKey) {
        ObjectNode root = baseLayoutJson(imageName, templateKey);
        root.set("layout", objectMapper.createObjectNode()
                .put("type", "unknown")
                .put("id", "invalid-root"));

        ArrayNode warnings = objectMapper.createArrayNode();
        warnings.add(issueNode(
                "INVALID_LAYOUT_TEMPLATE",
                "invalid-layout 是用于 image-page 失败状态展示的已知 mock 模板",
                "layout"));
        root.set("warnings", warnings);
        return root;
    }

    private ObjectNode baseLayoutJson(String imageName, String templateKey) {
        ObjectNode root = objectMapper.createObjectNode();
        root.put("version", "0.1");

        ObjectNode page = objectMapper.createObjectNode();
        page.put("title", templateKey + " image page mock");
        root.set("page", page);

        ObjectNode source = objectMapper.createObjectNode();
        source.put("type", "image-page-mock");
        source.put("imageName", imageName);
        source.put("templateKey", templateKey);
        root.set("source", source);

        ObjectNode tokens = objectMapper.createObjectNode();
        tokens.set("colors", objectMapper.createObjectNode()
                .put("primary", "#0f766e")
                .put("text", "#1f2937")
                .put("surface", "#f8fafc"));
        tokens.set("spacing", objectMapper.createObjectNode()
                .put("md", "16px")
                .put("lg", "24px"));
        root.set("tokens", tokens);

        root.set("assets", objectMapper.createArrayNode());
        root.set("responsive", objectMapper.createObjectNode()
                .put("strategy", "mock-responsive"));
        root.set("assumptions", objectMapper.createArrayNode()
                .add("imageName 仅作为 mock 元信息，后端未上传真实图片"));
        root.set("warnings", objectMapper.createArrayNode());
        return root;
    }

    private ObjectNode layoutNode(String templateKey) {
        if ("card-list".equals(templateKey)) {
            return cardListLayout();
        }
        return landingBasicLayout();
    }

    private ObjectNode landingBasicLayout() {
        ObjectNode layout = objectMapper.createObjectNode();
        layout.put("type", "page");
        layout.put("id", "page-root");

        ArrayNode children = objectMapper.createArrayNode();
        ObjectNode section = objectMapper.createObjectNode();
        section.put("type", "section");
        section.put("id", "hero-section");
        section.set("children", objectMapper.createArrayNode()
                .add(textNode("hero-title", "h1", "Mock Image Page"))
                .add(textNode("hero-copy", "p", "Safe generated page mock content for preview.")));
        children.add(section);
        layout.set("children", children);
        return layout;
    }

    private ObjectNode cardListLayout() {
        ObjectNode layout = objectMapper.createObjectNode();
        layout.put("type", "page");
        layout.put("id", "page-root");

        ObjectNode list = objectMapper.createObjectNode();
        list.put("type", "list");
        list.put("id", "card-list");
        list.set("children", objectMapper.createArrayNode()
                .add(cardNode("card-1", "Mock Card One"))
                .add(cardNode("card-2", "Mock Card Two")));

        layout.set("children", objectMapper.createArrayNode().add(list));
        return layout;
    }

    private ObjectNode cardNode(String id, String content) {
        ObjectNode card = objectMapper.createObjectNode();
        card.put("type", "card");
        card.put("id", id);
        card.set("children", objectMapper.createArrayNode()
                .add(textNode(id + "-title", "h2", content)));
        return card;
    }

    private ObjectNode textNode(String id, String role, String content) {
        ObjectNode text = objectMapper.createObjectNode();
        text.put("type", "text");
        text.put("id", id);
        text.put("role", role);
        text.put("content", content);
        return text;
    }

    private ObjectNode issueNode(String code, String message, String path) {
        ObjectNode issue = objectMapper.createObjectNode();
        issue.put("code", code);
        issue.put("message", message);
        issue.put("path", path);
        return issue;
    }

    private ImagePageGeneratedArtifact successGeneratedPageArtifact(String templateKey) {
        if ("card-list".equals(templateKey)) {
            return new ImagePageGeneratedArtifact(
                    "SUCCESS",
                    "<div class=\"mock-page\"><ul class=\"mock-card-list\"><li class=\"mock-card\">Mock Card One</li><li class=\"mock-card\">Mock Card Two</li></ul></div>",
                    ".mock-page { padding: 24px; background: #f8fafc; color: #1f2937; } .mock-card-list { display: grid; gap: 16px; list-style: none; padding: 0; margin: 0; } .mock-card { border: 1px solid #cbd5e1; border-radius: 12px; padding: 16px; background: #ffffff; }",
                    "<template><div class=\"mock-page\"><ul class=\"mock-card-list\"><li class=\"mock-card\">Mock Card One</li><li class=\"mock-card\">Mock Card Two</li></ul></div></template>");
        }

        return new ImagePageGeneratedArtifact(
                "SUCCESS",
                "<section class=\"mock-page\"><div class=\"mock-hero\"><h1>Mock Image Page</h1><p>Safe generated page mock content for preview.</p></div></section>",
                ".mock-page { padding: 32px; background: #f8fafc; color: #1f2937; } .mock-hero { max-width: 640px; } .mock-hero h1 { margin: 0 0 12px; font-size: 32px; } .mock-hero p { margin: 0; line-height: 1.6; }",
                "<template><section class=\"mock-page\"><div class=\"mock-hero\"><h1>Mock Image Page</h1><p>Safe generated page mock content for preview.</p></div></section></template>");
    }
}
