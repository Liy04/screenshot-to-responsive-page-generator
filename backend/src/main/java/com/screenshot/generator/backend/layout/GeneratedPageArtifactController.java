package com.screenshot.generator.backend.layout;

import com.fasterxml.jackson.databind.JsonNode;
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
public class GeneratedPageArtifactController {

    private final MockStorageService mockStorageService;

    public GeneratedPageArtifactController(MockStorageService mockStorageService) {
        this.mockStorageService = mockStorageService;
    }

    @PutMapping("/api/dev/generation-jobs/{jobId}/artifacts/generated-page")
    public ApiResponse<GeneratedPageArtifactSaveResponse> saveGeneratedPageArtifact(
            @PathVariable String jobId,
            @RequestBody(required = false) JsonNode artifactJson) {
        return ApiResponse.success(mockStorageService.saveGeneratedPageArtifact(jobId, artifactJson));
    }

    @GetMapping("/api/dev/generation-jobs/{jobId}/artifacts/generated-page")
    public ApiResponse<JsonNode> getGeneratedPageArtifact(@PathVariable String jobId) {
        return ApiResponse.success(mockStorageService.getGeneratedPageArtifact(jobId));
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
