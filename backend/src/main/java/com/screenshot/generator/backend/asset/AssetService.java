package com.screenshot.generator.backend.asset;

import java.io.IOException;
import java.io.InputStream;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.StandardCopyOption;
import java.util.Locale;
import java.util.Map;
import java.util.Set;
import java.util.UUID;
import java.util.concurrent.ConcurrentHashMap;

import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

@Service
public class AssetService {

    private static final long MAX_FILE_SIZE = 10L * 1024L * 1024L;
    private static final Set<String> SUPPORTED_EXTENSIONS = Set.of("png", "jpg", "jpeg", "webp");
    private static final Map<String, String> SUPPORTED_CONTENT_TYPES = Map.of(
            "image/png", "png",
            "image/jpeg", "jpg",
            "image/webp", "webp");

    private final Map<String, AssetUploadResponse> assets = new ConcurrentHashMap<>();
    private final Path uploadDirectory;

    public AssetService() {
        this.uploadDirectory = Path.of("uploads").toAbsolutePath().normalize();
    }

    public AssetUploadResponse upload(MultipartFile file) {
        validate(file);

        String contentType = normalizeContentType(file.getContentType());
        String extension = getExtension(file.getOriginalFilename());
        String assetId = "asset_" + UUID.randomUUID().toString().replace("-", "");
        String storedFileName = assetId + "." + extension;
        Path targetPath = uploadDirectory.resolve(storedFileName).normalize();

        if (!targetPath.startsWith(uploadDirectory)) {
            throw new IllegalArgumentException("文件名不合法");
        }

        try {
            Files.createDirectories(uploadDirectory);
            try (InputStream inputStream = file.getInputStream()) {
                Files.copy(inputStream, targetPath, StandardCopyOption.REPLACE_EXISTING);
            }
        } catch (IOException exception) {
            throw new IllegalStateException("文件保存失败", exception);
        }

        AssetUploadResponse response = new AssetUploadResponse(
                assetId,
                storedFileName,
                "/uploads/" + storedFileName,
                contentType,
                file.getSize());
        assets.put(assetId, response);
        return response;
    }

    public boolean exists(String assetId) {
        return assetId != null && assets.containsKey(assetId);
    }

    private void validate(MultipartFile file) {
        if (file == null || file.isEmpty()) {
            throw new IllegalArgumentException("上传文件不能为空");
        }

        if (file.getSize() > MAX_FILE_SIZE) {
            throw new IllegalArgumentException("上传文件不能超过 10MB");
        }

        String contentType = normalizeContentType(file.getContentType());
        String extension = getExtension(file.getOriginalFilename());

        if (!SUPPORTED_CONTENT_TYPES.containsKey(contentType) || !SUPPORTED_EXTENSIONS.contains(extension)) {
            throw new IllegalArgumentException("只支持 PNG、JPG、JPEG、WebP 图片");
        }

        if ("image/png".equals(contentType) && !"png".equals(extension)) {
            throw new IllegalArgumentException("文件类型与扩展名不一致");
        }

        if ("image/jpeg".equals(contentType) && !Set.of("jpg", "jpeg").contains(extension)) {
            throw new IllegalArgumentException("文件类型与扩展名不一致");
        }

        if ("image/webp".equals(contentType) && !"webp".equals(extension)) {
            throw new IllegalArgumentException("文件类型与扩展名不一致");
        }
    }

    private String normalizeContentType(String contentType) {
        if (contentType == null || contentType.isBlank()) {
            return "";
        }
        return contentType.toLowerCase(Locale.ROOT);
    }

    private String getExtension(String originalFilename) {
        if (originalFilename == null || originalFilename.isBlank()) {
            return "";
        }

        int dotIndex = originalFilename.lastIndexOf('.');
        if (dotIndex < 0 || dotIndex == originalFilename.length() - 1) {
            return "";
        }

        return originalFilename.substring(dotIndex + 1).toLowerCase(Locale.ROOT);
    }
}
