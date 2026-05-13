package com.screenshot.generator.backend.imagepage;

public record ImagePageUploadResponse(
        String jobId,
        String fileName,
        String sourceUrl) {
}
