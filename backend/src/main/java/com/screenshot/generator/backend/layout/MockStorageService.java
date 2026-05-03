package com.screenshot.generator.backend.layout;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.screenshot.generator.backend.common.ResourceNotFoundException;
import com.screenshot.generator.backend.common.StorageException;

import org.springframework.stereotype.Service;

@Service
public class MockStorageService {

    private static final String ARTIFACT_TYPE = "layout_json";
    private static final String DEFAULT_STATUS = "created";
    private static final Path STORAGE_DIRECTORY = Path.of("mock-data", "layout-artifacts");

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

        if (!jobId.matches("[A-Za-z0-9_-]+")) {
            throw new IllegalArgumentException("jobId 格式不合法");
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

    private String mockPath(String jobId) {
        return "mock-data/layout-artifacts/" + jobId + ".layout.json";
    }
}
