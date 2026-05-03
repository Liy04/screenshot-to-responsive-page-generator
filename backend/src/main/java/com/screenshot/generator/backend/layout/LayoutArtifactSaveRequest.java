package com.screenshot.generator.backend.layout;

import com.fasterxml.jackson.databind.JsonNode;

public record LayoutArtifactSaveRequest(
        JsonNode layoutJson,
        String status,
        String errorMessage) {
}
