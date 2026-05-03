package com.screenshot.generator.backend.layout;

public record LayoutArtifactSaveResponse(
        String jobId,
        String artifactType,
        String mockPath,
        String status) {
}
