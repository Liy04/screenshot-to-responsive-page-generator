package com.screenshot.generator.backend.layout;

import com.fasterxml.jackson.databind.JsonNode;

public record LayoutArtifactFilePayload(
        JsonNode layoutJson,
        String status,
        String errorMessage) {
}
