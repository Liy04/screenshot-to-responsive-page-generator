package com.screenshot.generator.backend.layout;

import java.util.List;

public record ImageLayoutJobResponse(
        String jobId,
        String status,
        String sourceType,
        String imageName,
        String templateKey,
        ImageLayoutArtifact layoutArtifact,
        List<ImageLayoutIssue> errors,
        List<ImageLayoutIssue> warnings) {
}
