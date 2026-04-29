package com.screenshot.generator.backend.generation;

public record GenerationJob(
        String jobId,
        String assetId,
        String mode,
        String targetStack,
        boolean responsive,
        String status,
        int progress,
        String createdAt) {
}
