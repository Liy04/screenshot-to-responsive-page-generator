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
public class ImageLayoutJobController {

    private final ImageLayoutJobService imageLayoutJobService;

    public ImageLayoutJobController(ImageLayoutJobService imageLayoutJobService) {
        this.imageLayoutJobService = imageLayoutJobService;
    }

    @PostMapping("/api/dev/image-layout-jobs")
    public ApiResponse<ImageLayoutJobResponse> createImageLayoutJob(
            @RequestBody(required = false) JsonNode requestJson) {
        return ApiResponse.success(imageLayoutJobService.createJob(requestJson));
    }

    @GetMapping("/api/dev/image-layout-jobs/{jobId}")
    public ApiResponse<ImageLayoutJobResponse> getImageLayoutJob(@PathVariable String jobId) {
        return ApiResponse.success(imageLayoutJobService.getJob(jobId));
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
