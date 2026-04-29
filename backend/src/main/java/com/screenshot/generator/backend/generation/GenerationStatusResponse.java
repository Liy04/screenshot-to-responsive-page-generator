package com.screenshot.generator.backend.generation;

public record GenerationStatusResponse(
        String jobId,
        String assetId,
        String mode,
        String status,
        int progress,
        String createdAt) {
}
