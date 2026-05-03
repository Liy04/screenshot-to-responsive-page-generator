package com.screenshot.generator.backend.layout;

import com.fasterxml.jackson.databind.JsonNode;

public record LayoutArtifactResponse(
        String jobId,
        String artifactType,
        JsonNode layoutJson,
        String status,
        String errorMessage) {
}
