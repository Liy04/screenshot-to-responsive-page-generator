package com.screenshot.generator.backend.layout;

import java.util.List;

public record ImagePageJobResponse(
        String jobId,
        String status,
        String sourceType,
        String imageName,
        String templateKey,
        ImageLayoutArtifact layoutArtifact,
        ImagePageGeneratedArtifact generatedPageArtifact,
        List<ImageLayoutIssue> errors,
        List<ImageLayoutIssue> warnings) {
}
