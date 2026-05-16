package com.screenshot.generator.backend.imagepage;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.node.MissingNode;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.time.Duration;
import java.util.Optional;

@Service
public class ImagePageGenerateService {

    private final ImagePageUploadService imagePageUploadService;
    private final ImagePageArtifactStorageService artifactStorageService;
    private final ImagePageWorkerRunner workerRunner;
    private final ObjectMapper objectMapper;
    private final String pythonCommand;
    private final String workerMode;
    private final boolean workerFallback;
    private final String configuredWorkerMainScript;
    private final Duration workerTimeout;

    public ImagePageGenerateService(
            ImagePageUploadService imagePageUploadService,
            ImagePageArtifactStorageService artifactStorageService,
            ImagePageWorkerRunner workerRunner,
            ObjectMapper objectMapper,
            @Value("${imagepage.worker.python-command:python}") String pythonCommand,
            @Value("${imagepage.worker.mode:real-ai}") String workerMode,
            @Value("${imagepage.worker.fallback:true}") boolean workerFallback,
            @Value("${imagepage.worker.main-script:}") String configuredWorkerMainScript,
            @Value("${imagepage.worker.timeout-seconds:30}") long workerTimeoutSeconds
    ) {
        this.imagePageUploadService = imagePageUploadService;
        this.artifactStorageService = artifactStorageService;
        this.workerRunner = workerRunner;
        this.objectMapper = objectMapper;
        this.pythonCommand = pythonCommand;
        this.workerMode = workerMode;
        this.workerFallback = workerFallback;
        this.configuredWorkerMainScript = configuredWorkerMainScript;
        this.workerTimeout = Duration.ofSeconds(Math.max(1L, workerTimeoutSeconds));
    }

    public ImagePageGenerateResponse generate(String jobId) {
        ImagePageSourceRecord sourceRecord = imagePageUploadService.getSource(jobId);
        Path jobDirectory = sourceRecord.filePath().toAbsolutePath().normalize().getParent();
        if (jobDirectory == null) {
            throw new IllegalStateException("未找到 job artifact 目录");
        }

        Optional<ImagePageGenerateResponse> cachedArtifact = artifactStorageService.loadSuccessfulArtifact(jobId, jobDirectory);
        if (cachedArtifact.isPresent()) {
            return cachedArtifact.get();
        }

        ImagePageWorkerExecutionResult executionResult = workerRunner.run(
                jobId,
                sourceRecord.filePath(),
                pythonCommand,
                resolveWorkerMainScript().toAbsolutePath().normalize().toString(),
                workerMode,
                workerFallback,
                workerTimeout,
                resolveRepoRoot()
        );

        JsonNode workerResult = parseWorkerResult(executionResult.stdout());

        if (executionResult.exitCode() != 0 && workerResult.isMissingNode()) {
            throw new IllegalStateException("Python Worker 执行失败，exitCode=" + executionResult.exitCode() + ", stderr=" + executionResult.stderr());
        }

        ImagePageGenerateResponse response = toResponse(jobId, executionResult, workerResult, false);

        if (executionResult.exitCode() != 0 && isBlank(response.status()) && isBlank(response.message())) {
            throw new IllegalStateException("Python Worker 执行失败，exitCode=" + executionResult.exitCode() + ", stderr=" + executionResult.stderr());
        }

        if (isSuccessfulArtifact(response)) {
            artifactStorageService.saveSuccessArtifact(jobDirectory, response);
            return withArtifactReuseFlag(response, false);
        }

        return response;
    }

    private ImagePageGenerateResponse toResponse(
            String fallbackJobId,
            ImagePageWorkerExecutionResult executionResult,
            JsonNode workerResult,
            boolean reused
    ) {
        JsonNode validationNode = getOptionalNode(workerResult, "validation");
        JsonNode layoutJsonNode = getOptionalNode(workerResult, "layoutJson");
        JsonNode warningsNode = getOptionalNode(validationNode, "warnings");
        JsonNode errorsNode = getOptionalNode(validationNode, "errors");

        return new ImagePageGenerateResponse(
                getText(workerResult, "jobId", fallbackJobId),
                getText(workerResult, "status", executionResult.exitCode() == 0 ? "SUCCESS" : "FAILED"),
                getText(workerResult, "mode", workerMode),
                getBoolean(workerResult, "fallbackUsed", workerFallback),
                textOrNull(workerResult, "fallbackReason"),
                getText(workerResult, "sourceType", ""),
                textOrNull(workerResult, "promptVersion"),
                layoutJsonNode,
                getText(workerResult, "previewHtml", ""),
                validationNode,
                warningsNode,
                errorsNode,
                getText(workerResult, "message", executionResult.exitCode() == 0 ? "Worker finished successfully." : "Worker returned a non-zero exit code."),
                artifactStorageService.buildArtifactInfo(reused),
                executionResult.exitCode(),
                executionResult.stdout(),
                executionResult.stderr(),
                workerResult.isMissingNode() ? null : workerResult
        );
    }

    private ImagePageGenerateResponse withArtifactReuseFlag(ImagePageGenerateResponse response, boolean reused) {
        return new ImagePageGenerateResponse(
                response.jobId(),
                response.status(),
                response.mode(),
                response.fallbackUsed(),
                response.fallbackReason(),
                response.sourceType(),
                response.promptVersion(),
                response.layoutJson(),
                response.previewHtml(),
                response.validation(),
                response.warnings(),
                response.errors(),
                response.message(),
                artifactStorageService.buildArtifactInfo(reused),
                response.exitCode(),
                response.stdout(),
                response.stderr(),
                response.workerResult()
        );
    }

    private boolean isSuccessfulArtifact(ImagePageGenerateResponse response) {
        return "SUCCESS".equals(response.status())
                && response.layoutJson() != null
                && response.previewHtml() != null
                && !response.previewHtml().isBlank();
    }

    private JsonNode parseWorkerResult(String stdout) {
        if (stdout == null || stdout.isBlank()) {
            return MissingNode.getInstance();
        }
        try {
            return objectMapper.readTree(stdout);
        } catch (IOException exception) {
            throw new IllegalStateException("解析 Python Worker JSON 输出失败: " + exception.getMessage(), exception);
        }
    }

    private Path resolveRepoRoot() {
        Path currentDirectory = Path.of("").toAbsolutePath().normalize();
        if (Files.isDirectory(currentDirectory.resolve("worker"))) {
            return currentDirectory;
        }
        Path parent = currentDirectory.getParent();
        if (parent != null && Files.isDirectory(parent.resolve("worker"))) {
            return parent;
        }
        throw new IllegalStateException("未找到 worker 目录，无法启动 Python Worker");
    }

    private Path resolveWorkerMainScript() {
        Path mainScript;
        if (configuredWorkerMainScript == null || configuredWorkerMainScript.isBlank()) {
            mainScript = resolveRepoRoot().resolve("worker").resolve("main.py");
        } else {
            Path configuredPath = Path.of(configuredWorkerMainScript);
            mainScript = configuredPath.isAbsolute() ? configuredPath : resolveRepoRoot().resolve(configuredPath);
        }
        mainScript = mainScript.toAbsolutePath().normalize();
        if (!Files.exists(mainScript)) {
            throw new IllegalStateException("未找到 worker/main.py: " + mainScript);
        }
        return mainScript;
    }

    private JsonNode getOptionalNode(JsonNode node, String fieldName) {
        if (node == null || node.isMissingNode()) {
            return null;
        }
        JsonNode value = node.get(fieldName);
        if (value == null || value.isNull() || value.isMissingNode()) {
            return null;
        }
        return value;
    }

    private String getText(JsonNode node, String fieldName, String fallbackValue) {
        JsonNode value = getOptionalNode(node, fieldName);
        if (value == null || !value.isValueNode()) {
            return fallbackValue;
        }
        String text = value.asText();
        return text == null ? fallbackValue : text;
    }

    private String textOrNull(JsonNode node, String fieldName) {
        JsonNode value = getOptionalNode(node, fieldName);
        return value == null ? null : value.asText();
    }

    private boolean getBoolean(JsonNode node, String fieldName, boolean fallbackValue) {
        JsonNode value = getOptionalNode(node, fieldName);
        return value == null ? fallbackValue : value.asBoolean(fallbackValue);
    }

    private boolean isBlank(String value) {
        return value == null || value.isBlank();
    }
}
