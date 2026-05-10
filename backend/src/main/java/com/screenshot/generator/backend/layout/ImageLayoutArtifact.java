package com.screenshot.generator.backend.layout;

import com.fasterxml.jackson.databind.JsonNode;

public record ImageLayoutArtifact(
        String status,
        JsonNode layoutJson) {
}
