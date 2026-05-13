package com.screenshot.generator.backend.imagepage;

import java.util.List;

import com.screenshot.generator.backend.common.ApiResponse;
import com.screenshot.generator.backend.common.ResourceNotFoundException;
import com.screenshot.generator.backend.common.StorageException;

import org.springframework.core.io.Resource;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.multipart.MultipartFile;

@RestController
public class ImagePageUploadController {

    private final ImagePageUploadService imagePageUploadService;
    private final ImagePageGenerateService imagePageGenerateService;

    public ImagePageUploadController(
            ImagePageUploadService imagePageUploadService,
            ImagePageGenerateService imagePageGenerateService
    ) {
        this.imagePageUploadService = imagePageUploadService;
        this.imagePageGenerateService = imagePageGenerateService;
    }

    @PostMapping("/api/image-page/upload")
    public ApiResponse<ImagePageUploadResponse> upload(@RequestParam("file") List<MultipartFile> files) {
        ImagePageUploadResponse response = imagePageUploadService.upload(files);
        return new ApiResponse<>(200, "upload success", response);
    }

    @GetMapping("/api/image-page/jobs/{jobId}/source")
    public ResponseEntity<Resource> getSource(@PathVariable String jobId) {
        ImagePageSourceRecord source = imagePageUploadService.getSource(jobId);
        Resource resource = imagePageUploadService.loadSourceResource(jobId);

        return ResponseEntity.ok()
                .contentType(MediaType.parseMediaType(source.contentType()))
                .header(HttpHeaders.CONTENT_DISPOSITION, "inline; filename=\"" + source.fileName() + "\"")
                .body(resource);
    }

    @PostMapping("/api/image-page/jobs/{jobId}/generate")
    public ApiResponse<ImagePageGenerateResponse> generate(@PathVariable String jobId) {
        ImagePageGenerateResponse response = imagePageGenerateService.generate(jobId);
        return ApiResponse.success(response);
    }

    @ExceptionHandler(IllegalArgumentException.class)
    public ResponseEntity<ApiResponse<Void>> handleBadRequest(IllegalArgumentException exception) {
        return ResponseEntity
                .status(HttpStatus.BAD_REQUEST)
                .body(ApiResponse.error(HttpStatus.BAD_REQUEST.value(), exception.getMessage()));
    }

    @ExceptionHandler(ResourceNotFoundException.class)
    public ResponseEntity<ApiResponse<Void>> handleNotFound(ResourceNotFoundException exception) {
        return ResponseEntity
                .status(HttpStatus.NOT_FOUND)
                .body(ApiResponse.error(HttpStatus.NOT_FOUND.value(), exception.getMessage()));
    }

    @ExceptionHandler(StorageException.class)
    public ResponseEntity<ApiResponse<Void>> handleStorageError(StorageException exception) {
        return ResponseEntity
                .status(HttpStatus.INTERNAL_SERVER_ERROR)
                .body(ApiResponse.error(HttpStatus.INTERNAL_SERVER_ERROR.value(), exception.getMessage()));
    }

    @ExceptionHandler(ImagePageWorkerTimeoutException.class)
    public ResponseEntity<ApiResponse<Void>> handleWorkerTimeout(ImagePageWorkerTimeoutException exception) {
        return ResponseEntity
                .status(HttpStatus.GATEWAY_TIMEOUT)
                .body(ApiResponse.error(HttpStatus.GATEWAY_TIMEOUT.value(), exception.getMessage()));
    }

    @ExceptionHandler(IllegalStateException.class)
    public ResponseEntity<ApiResponse<Void>> handleIllegalState(IllegalStateException exception) {
        return ResponseEntity
                .status(HttpStatus.INTERNAL_SERVER_ERROR)
                .body(ApiResponse.error(HttpStatus.INTERNAL_SERVER_ERROR.value(), exception.getMessage()));
    }
}
