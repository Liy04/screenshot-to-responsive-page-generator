package com.screenshot.generator.backend.generation;

public record GenerationResultResponse(
        String jobId,
        String artifactId,
        Object layoutJson,
        String vueCode,
        String cssCode) {
}
