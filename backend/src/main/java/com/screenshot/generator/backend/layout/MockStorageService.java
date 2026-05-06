package com.screenshot.generator.backend.layout;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.screenshot.generator.backend.common.ResourceNotFoundException;
import com.screenshot.generator.backend.common.StorageException;

import org.springframework.stereotype.Service;

@Service
public class MockStorageService {

    private static final String ARTIFACT_TYPE = "layout_json";
    private static final String GENERATED_PAGE_ARTIFACT_TYPE = "generated-page";
    private static final String DEFAULT_STATUS = "created";
    private static final int MAX_GENERATED_PAGE_ARTIFACT_BYTES = 2 * 1024 * 1024;
    private static final Path STORAGE_DIRECTORY = Path.of("mock-data", "layout-artifacts");
    private static final Path GENERATED_PAGE_STORAGE_DIRECTORY = Path.of("mock-data", "generated-page-artifacts");

    private final ObjectMapper objectMapper;

    public MockStorageService(ObjectMapper objectMapper) {
        this.objectMapper = objectMapper;
    }

    public LayoutArtifactSaveResponse saveLayoutArtifact(String jobId, LayoutArtifactSaveRequest request) {
        validateJobId(jobId);
        validateSaveRequest(request);

        String status = normalizeStatus(request.status());
        Path artifactPath = artifactPath(jobId);
        LayoutArtifactFilePayload payload = new LayoutArtifactFilePayload(
                request.layoutJson(),
                status,
                request.errorMessage());

        try {
            Files.createDirectories(absoluteStorageDirectory());
            objectMapper.writerWithDefaultPrettyPrinter().writeValue(artifactPath.toFile(), payload);
        } catch (IOException exception) {
            throw new StorageException("本地 mock 文件保存失败", exception);
        }

        return new LayoutArtifactSaveResponse(jobId, ARTIFACT_TYPE, mockPath(jobId), status);
    }

    public LayoutArtifactResponse getLayoutArtifact(String jobId) {
        validateJobId(jobId);

        Path artifactPath = artifactPath(jobId);
        if (!Files.exists(artifactPath)) {
            throw new ResourceNotFoundException("Layout JSON mock 文件不存在");
        }

        try {
            LayoutArtifactFilePayload payload = objectMapper.readValue(
                    artifactPath.toFile(),
                    LayoutArtifactFilePayload.class);
            return new LayoutArtifactResponse(
                    jobId,
                    ARTIFACT_TYPE,
                    payload.layoutJson(),
                    payload.status(),
                    payload.errorMessage());
        } catch (IOException exception) {
            throw new StorageException("本地 mock 文件读取失败", exception);
        }
    }

    public GeneratedPageArtifactSaveResponse saveGeneratedPageArtifact(String jobId, JsonNode artifactJson) {
        validateJobId(jobId);
        validateGeneratedPageArtifact(artifactJson);

        byte[] artifactBytes = serializeArtifact(artifactJson);
        if (artifactBytes.length > MAX_GENERATED_PAGE_ARTIFACT_BYTES) {
            throw new IllegalArgumentException("generated-page artifact 不能超过 2MB");
        }

        Path artifactPath = generatedPageArtifactPath(jobId);
        try {
            Files.createDirectories(absoluteGeneratedPageStorageDirectory());
            Files.write(artifactPath, artifactBytes);
        } catch (IOException exception) {
            throw new StorageException("generated-page artifact 保存失败", exception);
        }

        return new GeneratedPageArtifactSaveResponse(
                jobId,
                GENERATED_PAGE_ARTIFACT_TYPE,
                generatedPageMockPath(jobId),
                artifactJson.path("status").asText(null));
    }

    public JsonNode getGeneratedPageArtifact(String jobId) {
        validateJobId(jobId);

        Path artifactPath = generatedPageArtifactPath(jobId);
        if (!Files.exists(artifactPath)) {
            throw new ResourceNotFoundException("generated-page artifact 不存在");
        }

        try {
            return objectMapper.readTree(artifactPath.toFile());
        } catch (IOException exception) {
            throw new StorageException("generated-page artifact 读取失败", exception);
        }
    }

    private void validateSaveRequest(LayoutArtifactSaveRequest request) {
        if (request == null) {
            throw new IllegalArgumentException("请求体不能为空");
        }

        if (request.layoutJson() == null || request.layoutJson().isNull()
                || (request.layoutJson().isObject() && request.layoutJson().isEmpty())) {
            throw new IllegalArgumentException("layoutJson 不能为空");
        }
    }

    private void validateJobId(String jobId) {
        if (jobId == null || jobId.isBlank()) {
            throw new IllegalArgumentException("jobId 不能为空");
        }

        if (!jobId.matches("[A-Za-z0-9_-]{1,64}")) {
            throw new IllegalArgumentException("jobId 格式不合法");
        }
    }

    private void validateGeneratedPageArtifact(JsonNode artifactJson) {
        if (artifactJson == null || artifactJson.isNull()) {
            throw new IllegalArgumentException("generated-page artifact 不能为空");
        }

        if (!artifactJson.isObject()) {
            throw new IllegalArgumentException("generated-page artifact 必须是 JSON 对象");
        }

        if (artifactJson.isEmpty()) {
            throw new IllegalArgumentException("generated-page artifact 不能为空");
        }
    }

    private byte[] serializeArtifact(JsonNode artifactJson) {
        try {
            return objectMapper.writerWithDefaultPrettyPrinter().writeValueAsBytes(artifactJson);
        } catch (IOException exception) {
            throw new StorageException("generated-page artifact 序列化失败", exception);
        }
    }

    private String normalizeStatus(String status) {
        if (status == null || status.isBlank()) {
            return DEFAULT_STATUS;
        }
        return status;
    }

    private Path artifactPath(String jobId) {
        Path targetPath = absoluteStorageDirectory().resolve(jobId + ".layout.json").normalize();
        if (!targetPath.startsWith(absoluteStorageDirectory())) {
            throw new IllegalArgumentException("jobId 格式不合法");
        }
        return targetPath;
    }

    private Path absoluteStorageDirectory() {
        return STORAGE_DIRECTORY.toAbsolutePath().normalize();
    }

    private Path generatedPageArtifactPath(String jobId) {
        Path targetPath = absoluteGeneratedPageStorageDirectory()
                .resolve(jobId + ".generated-page.json")
                .normalize();
        if (!targetPath.startsWith(absoluteGeneratedPageStorageDirectory())) {
            throw new IllegalArgumentException("jobId 格式不合法");
        }
        return targetPath;
    }

    private Path absoluteGeneratedPageStorageDirectory() {
        return GENERATED_PAGE_STORAGE_DIRECTORY.toAbsolutePath().normalize();
    }

    private String mockPath(String jobId) {
        return "mock-data/layout-artifacts/" + jobId + ".layout.json";
    }

    private String generatedPageMockPath(String jobId) {
        return "mock-data/generated-page-artifacts/" + jobId + ".generated-page.json";
    }
}
