package com.screenshot.generator.backend.imagepage;

import java.nio.file.Path;
import java.time.Duration;

public interface ImagePageWorkerRunner {

    ImagePageWorkerExecutionResult run(
            String jobId,
            Path imagePath,
            String pythonCommand,
            String workerMainScript,
            String mode,
            boolean fallback,
            Duration timeout,
            Path repoRoot
    );
}
