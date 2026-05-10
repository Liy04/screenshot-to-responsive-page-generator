package com.screenshot.generator.backend.layout;

import com.fasterxml.jackson.databind.JsonNode;
import com.screenshot.generator.backend.common.ApiResponse;
import com.screenshot.generator.backend.common.ResourceNotFoundException;

import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class ImagePageJobController {

    private final ImagePageJobService imagePageJobService;

    public ImagePageJobController(ImagePageJobService imagePageJobService) {
        this.imagePageJobService = imagePageJobService;
    }

    @PostMapping("/api/dev/image-page-jobs")
    public ApiResponse<ImagePageJobResponse> createImagePageJob(
            @RequestBody(required = false) JsonNode requestJson) {
        return ApiResponse.success(imagePageJobService.createJob(requestJson));
    }

    @GetMapping("/api/dev/image-page-jobs/{jobId}")
    public ApiResponse<ImagePageJobResponse> getImagePageJob(@PathVariable String jobId) {
        return ApiResponse.success(imagePageJobService.getJob(jobId));
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
}
