package com.screenshot.generator.backend.imagepage;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.node.MissingNode;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

import java.io.IOException;
import java.io.InputStream;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.time.Duration;
import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.Future;
import java.util.concurrent.TimeUnit;

@Service
public class ImagePageGenerateService {

    private final ImagePageUploadService imagePageUploadService;
    private final ObjectMapper objectMapper;
    private final String pythonCommand;
    private final String workerMode;
    private final boolean workerFallback;
    private final String configuredWorkerMainScript;
    private final Duration workerTimeout;

    public ImagePageGenerateService(
            ImagePageUploadService imagePageUploadService,
            ObjectMapper objectMapper,
            @Value("${imagepage.worker.python-command:python}") String pythonCommand,
            @Value("${imagepage.worker.mode:real-ai}") String workerMode,
            @Value("${imagepage.worker.fallback:true}") boolean workerFallback,
            @Value("${imagepage.worker.main-script:}") String configuredWorkerMainScript,
            @Value("${imagepage.worker.timeout-seconds:30}") long workerTimeoutSeconds
    ) {
        this.imagePageUploadService = imagePageUploadService;
        this.objectMapper = objectMapper;
        this.pythonCommand = pythonCommand;
        this.workerMode = workerMode;
        this.workerFallback = workerFallback;
        this.configuredWorkerMainScript = configuredWorkerMainScript;
        this.workerTimeout = Duration.ofSeconds(Math.max(1L, workerTimeoutSeconds));
    }

    public ImagePageGenerateResponse generate(String jobId) {
        ImagePageSourceRecord sourceRecord = imagePageUploadService.getSource(jobId);
        Path workerMainScript = resolveWorkerMainScript();

        ProcessBuilder processBuilder = new ProcessBuilder(buildCommand(jobId, sourceRecord.filePath(), workerMainScript));
        processBuilder.directory(resolveRepoRoot().toFile());
        processBuilder.environment().put("PYTHONIOENCODING", "utf-8");

        Process process;
        try {
            process = processBuilder.start();
        } catch (IOException exception) {
            throw new IllegalStateException("Python Worker 启动失败: " + exception.getMessage(), exception);
        }

        ProcessOutput processOutput = readProcessOutput(process);

        boolean finished;
        try {
            finished = process.waitFor(workerTimeout.toMillis(), TimeUnit.MILLISECONDS);
        } catch (InterruptedException exception) {
            Thread.currentThread().interrupt();
            process.destroyForcibly();
            processOutput.close();
            throw new IllegalStateException("等待 Python Worker 结果时被中断", exception);
        }

        if (!finished) {
            process.destroyForcibly();
            processOutput.close();
            throw new ImagePageWorkerTimeoutException("Python Worker 执行超时，超过 " + workerTimeout.toSeconds() + " 秒");
        }

        String stdout = processOutput.stdout();
        String stderr = processOutput.stderr();
        int exitCode = process.exitValue();
        JsonNode workerResult = parseWorkerResult(stdout);

        if (exitCode != 0 && workerResult.isMissingNode()) {
            throw new IllegalStateException("Python Worker 执行失败，exitCode=" + exitCode + ", stderr=" + stderr);
        }

        ImagePageGenerateResponse response = toResponse(jobId, exitCode, stdout, stderr, workerResult);

        if (exitCode != 0 && isBlank(response.status()) && isBlank(response.message())) {
            throw new IllegalStateException("Python Worker 执行失败，exitCode=" + exitCode + ", stderr=" + stderr);
        }

        return response;
    }

    private List<String> buildCommand(String jobId, Path imagePath, Path workerMainScript) {
        List<String> command = new ArrayList<>();
        command.add(pythonCommand);
        command.add(workerMainScript.toAbsolutePath().normalize().toString());
        command.add("--job-id");
        command.add(jobId.toString());
        command.add("--image-path");
        command.add(imagePath.toAbsolutePath().normalize().toString());
        command.add("--mode");
        command.add(workerMode);
        command.add("--fallback");
        command.add(Boolean.toString(workerFallback));
        return command;
    }

    private ImagePageGenerateResponse toResponse(
            String fallbackJobId,
            int exitCode,
            String stdout,
            String stderr,
            JsonNode workerResult
    ) {
        JsonNode validationNode = getOptionalNode(workerResult, "validation");
        JsonNode layoutJsonNode = getOptionalNode(workerResult, "layoutJson");

        return new ImagePageGenerateResponse(
                getText(workerResult, "jobId", fallbackJobId),
                getText(workerResult, "status", exitCode == 0 ? "SUCCESS" : "FAILED"),
                getText(workerResult, "mode", workerMode),
                getBoolean(workerResult, "fallbackUsed", workerFallback),
                getText(workerResult, "sourceType", ""),
                layoutJsonNode,
                getText(workerResult, "previewHtml", ""),
                validationNode,
                getText(workerResult, "message", exitCode == 0 ? "Worker finished successfully." : "Worker returned a non-zero exit code."),
                exitCode,
                stdout,
                stderr,
                workerResult.isMissingNode() ? null : workerResult
        );
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

    private String readStream(InputStream inputStream) {
        try {
            return new String(inputStream.readAllBytes(), StandardCharsets.UTF_8).trim();
        } catch (IOException exception) {
            throw new IllegalStateException("读取 Python Worker 输出流失败: " + exception.getMessage(), exception);
        }
    }

    private ProcessOutput readProcessOutput(Process process) {
        ExecutorService executorService = Executors.newFixedThreadPool(2);
        try {
            Future<String> stdoutFuture = executorService.submit(() -> readStream(process.getInputStream()));
            Future<String> stderrFuture = executorService.submit(() -> readStream(process.getErrorStream()));
            return new ProcessOutput(stdoutFuture, stderrFuture, executorService);
        } catch (RuntimeException exception) {
            executorService.shutdownNow();
            throw exception;
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

    private boolean getBoolean(JsonNode node, String fieldName, boolean fallbackValue) {
        JsonNode value = getOptionalNode(node, fieldName);
        return value == null ? fallbackValue : value.asBoolean(fallbackValue);
    }

    private boolean isBlank(String value) {
        return value == null || value.isBlank();
    }

    private record ProcessOutput(Future<String> stdoutFuture, Future<String> stderrFuture, ExecutorService executorService) {

        String stdout() {
            return get(stdoutFuture);
        }

        String stderr() {
            try {
                return get(stderrFuture);
            } finally {
                close();
            }
        }

        void close() {
            executorService.shutdownNow();
        }

        private String get(Future<String> future) {
            try {
                return future.get();
            } catch (InterruptedException exception) {
                Thread.currentThread().interrupt();
                throw new IllegalStateException("读取 Python Worker 输出时被中断", exception);
            } catch (ExecutionException exception) {
                throw new IllegalStateException("读取 Python Worker 输出失败: " + exception.getCause().getMessage(), exception.getCause());
            }
        }
    }
}
