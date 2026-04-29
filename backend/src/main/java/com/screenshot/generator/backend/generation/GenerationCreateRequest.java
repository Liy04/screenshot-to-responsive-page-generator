package com.screenshot.generator.backend.generation;

public record GenerationCreateRequest(
        String assetId,
        String mode,
        String targetStack,
        Boolean responsive) {
}
