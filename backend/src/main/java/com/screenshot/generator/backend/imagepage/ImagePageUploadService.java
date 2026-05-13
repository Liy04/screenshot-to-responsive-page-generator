package com.screenshot.generator.backend.imagepage;

import java.io.IOException;
import java.io.InputStream;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.StandardCopyOption;
import java.util.List;
import java.util.Locale;
import java.util.Map;
import java.util.Set;
import java.util.UUID;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.ConcurrentMap;

import com.screenshot.generator.backend.common.ResourceNotFoundException;
import com.screenshot.generator.backend.common.StorageException;

import org.springframework.core.io.FileSystemResource;
import org.springframework.core.io.Resource;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

@Service
public class ImagePageUploadService {

    private static final long MAX_FILE_SIZE = 5L * 1024L * 1024L;
    private static final Set<String> SUPPORTED_EXTENSIONS = Set.of("png", "jpg", "jpeg", "webp");
    private static final Map<String, String> SUPPORTED_CONTENT_TYPES = Map.of(
            "image/png", "png",
            "image/jpeg", "jpg",
            "image/webp", "webp");
    private static final String JOB_ID_PATTERN = "[A-Za-z0-9_-]{1,64}";

    private final ConcurrentMap<String, ImagePageSourceRecord> records = new ConcurrentHashMap<>();
    private final Path storageRoot;

    public ImagePageUploadService() {
        this.storageRoot = Path.of("storage", "temp").toAbsolutePath().normalize();
    }

    public ImagePageUploadResponse upload(List<MultipartFile> files) {
        validateFileList(files);

        MultipartFile file = files.get(0);
        validateFile(file);

        String contentType = normalizeContentType(file.getContentType());
        String extension = getExtension(file.getOriginalFilename());
        String originalFileName = safeOriginalFileName(file.getOriginalFilename(), extension);
        String jobId = nextJobId();

        Path jobDirectory = storageRoot.resolve(jobId).normalize();
        Path targetPath = jobDirectory.resolve("input." + extension).normalize();
        validatePath(jobDirectory);
        validatePath(targetPath);

        try {
            Files.createDirectories(jobDirectory);
            try (InputStream inputStream = file.getInputStream()) {
                Files.copy(inputStream, targetPath, StandardCopyOption.REPLACE_EXISTING);
            }
        } catch (IOException exception) {
            throw new StorageException("图片保存失败", exception);
        }

        records.put(jobId, new ImagePageSourceRecord(jobId, originalFileName, contentType, targetPath));
        return new ImagePageUploadResponse(jobId, originalFileName, sourceUrl(jobId));
    }

    public ImagePageSourceRecord getSource(String jobId) {
        validateJobId(jobId);

        ImagePageSourceRecord record = records.get(jobId);
        if (record == null || !Files.exists(record.filePath())) {
            throw new ResourceNotFoundException("原图不存在");
        }
        return record;
    }

    public Resource loadSourceResource(String jobId) {
        return new FileSystemResource(getSource(jobId).filePath());
    }

    private void validateFileList(List<MultipartFile> files) {
        if (files == null || files.isEmpty()) {
            throw new IllegalArgumentException("上传文件不能为空");
        }

        if (files.size() != 1) {
            throw new IllegalArgumentException("只支持单张图片上传");
        }
    }

    private void validateFile(MultipartFile file) {
        if (file == null || file.isEmpty()) {
            throw new IllegalArgumentException("上传文件不能为空");
        }

        if (file.getSize() > MAX_FILE_SIZE) {
            throw new IllegalArgumentException("上传文件不能超过 5MB");
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

    private void validateJobId(String jobId) {
        if (jobId == null || jobId.isBlank()) {
            throw new IllegalArgumentException("jobId 不能为空");
        }

        if (!jobId.matches(JOB_ID_PATTERN)) {
            throw new IllegalArgumentException("jobId 格式不合法");
        }
    }

    private void validatePath(Path path) {
        if (!path.startsWith(storageRoot)) {
            throw new IllegalArgumentException("jobId 格式不合法");
        }
    }

    private String nextJobId() {
        return "imgjob_" + UUID.randomUUID().toString().replace("-", "");
    }

    private String sourceUrl(String jobId) {
        return "/api/image-page/jobs/" + jobId + "/source";
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

    private String safeOriginalFileName(String originalFilename, String fallbackExtension) {
        if (originalFilename == null || originalFilename.isBlank()) {
            return "input." + fallbackExtension;
        }

        String safeName = Path.of(originalFilename).getFileName().toString();
        if (safeName.isBlank()) {
            return "input." + fallbackExtension;
        }
        return safeName;
    }
}
