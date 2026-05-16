package com.screenshot.generator.backend.imagepage;

import com.fasterxml.jackson.databind.JsonNode;

public record ImagePageGenerateResponse(
        String jobId,
        String status,
        String mode,
        boolean fallbackUsed,
        String fallbackReason,
        String sourceType,
        String promptVersion,
        JsonNode layoutJson,
        String previewHtml,
        JsonNode validation,
        JsonNode warnings,
        JsonNode errors,
        String message,
        ImagePageArtifactInfo artifact,
        int exitCode,
        String stdout,
        String stderr,
        JsonNode workerResult
) {
}
