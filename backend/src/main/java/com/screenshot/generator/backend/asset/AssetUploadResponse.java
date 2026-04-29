package com.screenshot.generator.backend.asset;

public record AssetUploadResponse(
        String assetId,
        String fileName,
        String fileUrl,
        String contentType,
        long size) {
}
