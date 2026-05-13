package com.screenshot.generator.backend.imagepage;

import com.fasterxml.jackson.databind.JsonNode;

public record ImagePageGenerateResponse(
        String jobId,
        String status,
        String mode,
        boolean fallbackUsed,
        String sourceType,
        JsonNode layoutJson,
        String previewHtml,
        JsonNode validation,
        String message,
        int exitCode,
        String stdout,
        String stderr,
        JsonNode workerResult
) {
}
