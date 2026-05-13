package com.screenshot.generator.backend.imagepage;

import java.nio.file.Path;

record ImagePageSourceRecord(
        String jobId,
        String fileName,
        String contentType,
        Path filePath) {
}
