package com.screenshot.generator.backend.imagepage;

public record ImagePageWorkerExecutionResult(
        int exitCode,
        String stdout,
        String stderr
) {
}
