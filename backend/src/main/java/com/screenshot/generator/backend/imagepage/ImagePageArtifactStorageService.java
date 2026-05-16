package com.screenshot.generator.backend.imagepage;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.node.ObjectNode;
import org.springframework.stereotype.Service;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.time.OffsetDateTime;
import java.util.Optional;

@Service
public class ImagePageArtifactStorageService {

    private static final String LAYOUT_FILE_NAME = "layout.json";
    private static final String PREVIEW_FILE_NAME = "preview.html";
    private static final String METADATA_FILE_NAME = "metadata.json";

    private final ObjectMapper objectMapper;

    public ImagePageArtifactStorageService(ObjectMapper objectMapper) {
        this.objectMapper = objectMapper;
    }

    public Optional<ImagePageGenerateResponse> loadSuccessfulArtifact(String jobId, Path jobDirectory) {
        validateJobDirectory(jobDirectory);

        Path metadataPath = jobDirectory.resolve(METADATA_FILE_NAME).normalize();
        Path layoutPath = jobDirectory.resolve(LAYOUT_FILE_NAME).normalize();
        Path previewPath = jobDirectory.resolve(PREVIEW_FILE_NAME).normalize();
        validateArtifactPath(jobDirectory, metadataPath);
        validateArtifactPath(jobDirectory, layoutPath);
        validateArtifactPath(jobDirectory, previewPath);

        if (!Files.exists(metadataPath) || !Files.exists(layoutPath) || !Files.exists(previewPath)) {
            return Optional.empty();
        }

        try {
            JsonNode metadata = objectMapper.readTree(Files.readString(metadataPath, StandardCharsets.UTF_8));
            if (!"SUCCESS".equals(metadata.path("status").asText())) {
                return Optional.empty();
            }

            JsonNode layoutJson = objectMapper.readTree(Files.readString(layoutPath, StandardCharsets.UTF_8));
            String previewHtml = Files.readString(previewPath, StandardCharsets.UTF_8);
            JsonNode validation = getOptionalNode(metadata, "validation");
            JsonNode warnings = getOptionalNode(metadata, "warnings");
            JsonNode errors = getOptionalNode(metadata, "errors");

            return Optional.of(new ImagePageGenerateResponse(
                    metadata.path("jobId").asText(jobId),
                    metadata.path("status").asText("SUCCESS"),
                    metadata.path("mode").asText("real-ai"),
                    metadata.path("fallbackUsed").asBoolean(false),
                    textOrNull(metadata, "fallbackReason"),
                    metadata.path("sourceType").asText(""),
                    textOrNull(metadata, "promptVersion"),
                    layoutJson,
                    previewHtml,
                    validation,
                    warnings,
                    errors,
                    metadata.path("message").asText("Artifact loaded from local storage."),
                    new ImagePageArtifactInfo(true, LAYOUT_FILE_NAME, PREVIEW_FILE_NAME, METADATA_FILE_NAME),
                    metadata.path("exitCode").asInt(0),
                    "",
                    "",
                    getOptionalNode(metadata, "workerResult")
            ));
        } catch (IOException exception) {
            throw new IllegalStateException("读取本地 artifact 失败: " + exception.getMessage(), exception);
        }
    }

    public void saveSuccessArtifact(Path jobDirectory, ImagePageGenerateResponse response) {
        validateJobDirectory(jobDirectory);

        Path layoutPath = jobDirectory.resolve(LAYOUT_FILE_NAME).normalize();
        Path previewPath = jobDirectory.resolve(PREVIEW_FILE_NAME).normalize();
        Path metadataPath = jobDirectory.resolve(METADATA_FILE_NAME).normalize();
        validateArtifactPath(jobDirectory, layoutPath);
        validateArtifactPath(jobDirectory, previewPath);
        validateArtifactPath(jobDirectory, metadataPath);

        try {
            Files.createDirectories(jobDirectory);
            Files.writeString(layoutPath, objectMapper.writerWithDefaultPrettyPrinter().writeValueAsString(response.layoutJson()), StandardCharsets.UTF_8);
            Files.writeString(previewPath, response.previewHtml() == null ? "" : response.previewHtml(), StandardCharsets.UTF_8);
            Files.writeString(metadataPath, buildMetadata(response), StandardCharsets.UTF_8);
        } catch (IOException exception) {
            throw new IllegalStateException("保存本地 artifact 失败: " + exception.getMessage(), exception);
        }
    }

    public ImagePageArtifactInfo buildArtifactInfo(boolean reused) {
        return new ImagePageArtifactInfo(reused, LAYOUT_FILE_NAME, PREVIEW_FILE_NAME, METADATA_FILE_NAME);
    }

    private String buildMetadata(ImagePageGenerateResponse response) throws IOException {
        ObjectNode metadata = objectMapper.createObjectNode();
        metadata.put("jobId", response.jobId());
        metadata.put("status", response.status());
        metadata.put("mode", response.mode());
        metadata.put("fallbackUsed", response.fallbackUsed());
        if (response.fallbackReason() != null) {
            metadata.put("fallbackReason", response.fallbackReason());
        } else {
            metadata.putNull("fallbackReason");
        }
        metadata.put("sourceType", response.sourceType());
        if (response.promptVersion() != null) {
            metadata.put("promptVersion", response.promptVersion());
        } else {
            metadata.putNull("promptVersion");
        }
        if (response.validation() != null) {
            metadata.set("validation", response.validation());
        } else {
            metadata.putNull("validation");
        }
        if (response.warnings() != null) {
            metadata.set("warnings", response.warnings());
        } else {
            metadata.putArray("warnings");
        }
        if (response.errors() != null) {
            metadata.set("errors", response.errors());
        } else {
            metadata.putArray("errors");
        }
        metadata.put("message", response.message());
        metadata.put("generatedAt", OffsetDateTime.now().toString());
        metadata.put("exitCode", response.exitCode());
        if (response.workerResult() != null) {
            metadata.set("workerResult", response.workerResult());
        } else {
            metadata.putNull("workerResult");
        }
        return objectMapper.writerWithDefaultPrettyPrinter().writeValueAsString(metadata);
    }

    private void validateJobDirectory(Path jobDirectory) {
        Path normalized = jobDirectory.toAbsolutePath().normalize();
        if (!normalized.getFileName().toString().matches("[A-Za-z0-9_-]{1,64}")) {
            throw new IllegalArgumentException("jobId 格式不合法");
        }
    }

    private void validateArtifactPath(Path jobDirectory, Path artifactPath) {
        if (!artifactPath.normalize().startsWith(jobDirectory.toAbsolutePath().normalize())) {
            throw new IllegalArgumentException("jobId 格式不合法");
        }
    }

    private JsonNode getOptionalNode(JsonNode node, String fieldName) {
        if (node == null) {
            return null;
        }
        JsonNode value = node.get(fieldName);
        if (value == null || value.isNull() || value.isMissingNode()) {
            return null;
        }
        return value;
    }

    private String textOrNull(JsonNode node, String fieldName) {
        JsonNode value = getOptionalNode(node, fieldName);
        return value == null ? null : value.asText();
    }
}
