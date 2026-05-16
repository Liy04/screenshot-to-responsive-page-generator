package com.screenshot.generator.backend.imagepage;

public record ImagePageArtifactInfo(
        boolean reused,
        String layoutFileName,
        String previewFileName,
        String metadataFileName
) {
}
