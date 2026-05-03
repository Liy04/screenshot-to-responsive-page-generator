package com.screenshot.generator.backend.layout;

import com.screenshot.generator.backend.common.ApiResponse;
import com.screenshot.generator.backend.common.ResourceNotFoundException;
import com.screenshot.generator.backend.common.StorageException;

import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class LayoutArtifactController {

    private final MockStorageService mockStorageService;

    public LayoutArtifactController(MockStorageService mockStorageService) {
        this.mockStorageService = mockStorageService;
    }

    @PutMapping("/api/dev/generation-jobs/{jobId}/artifacts/layout-json")
    public ApiResponse<LayoutArtifactSaveResponse> saveLayoutArtifact(
            @PathVariable String jobId,
            @RequestBody(required = false) LayoutArtifactSaveRequest request) {
        return ApiResponse.success(mockStorageService.saveLayoutArtifact(jobId, request));
    }

    @GetMapping("/api/dev/generation-jobs/{jobId}/artifacts/layout-json")
    public ApiResponse<LayoutArtifactResponse> getLayoutArtifact(@PathVariable String jobId) {
        return ApiResponse.success(mockStorageService.getLayoutArtifact(jobId));
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
}
