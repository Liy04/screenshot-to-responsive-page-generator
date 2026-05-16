package com.screenshot.generator.backend.imagepage;

import org.springframework.stereotype.Component;

import java.io.IOException;
import java.io.InputStream;
import java.nio.charset.StandardCharsets;
import java.nio.file.Path;
import java.time.Duration;
import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.Future;
import java.util.concurrent.TimeUnit;

@Component
public class ProcessBuilderImagePageWorkerRunner implements ImagePageWorkerRunner {

    @Override
    public ImagePageWorkerExecutionResult run(
            String jobId,
            Path imagePath,
            String pythonCommand,
            String workerMainScript,
            String mode,
            boolean fallback,
            Duration timeout,
            Path repoRoot
    ) {
        List<String> command = new ArrayList<>();
        command.add(pythonCommand);
        command.add(workerMainScript);
        command.add("--job-id");
        command.add(jobId);
        command.add("--image-path");
        command.add(imagePath.toAbsolutePath().normalize().toString());
        command.add("--mode");
        command.add(mode);
        command.add("--fallback");
        command.add(Boolean.toString(fallback));

        ProcessBuilder processBuilder = new ProcessBuilder(command);
        processBuilder.directory(repoRoot.toFile());
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
            finished = process.waitFor(timeout.toMillis(), TimeUnit.MILLISECONDS);
        } catch (InterruptedException exception) {
            Thread.currentThread().interrupt();
            process.destroyForcibly();
            processOutput.close();
            throw new IllegalStateException("等待 Python Worker 结果时被中断", exception);
        }

        if (!finished) {
            process.destroyForcibly();
            processOutput.close();
            throw new ImagePageWorkerTimeoutException("Python Worker 执行超时，超过 " + timeout.toSeconds() + " 秒");
        }

        return new ImagePageWorkerExecutionResult(
                process.exitValue(),
                processOutput.stdout(),
                processOutput.stderr()
        );
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

    private String readStream(InputStream inputStream) {
        try {
            return new String(inputStream.readAllBytes(), StandardCharsets.UTF_8).trim();
        } catch (IOException exception) {
            throw new IllegalStateException("读取 Python Worker 输出流失败: " + exception.getMessage(), exception);
        }
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
                Throwable cause = exception.getCause();
                String message = cause == null ? exception.getMessage() : cause.getMessage();
                throw new IllegalStateException("读取 Python Worker 输出失败: " + message, cause == null ? exception : cause);
            }
        }
    }
}
