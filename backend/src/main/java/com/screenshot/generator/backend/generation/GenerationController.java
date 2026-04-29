package com.screenshot.generator.backend.generation;

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
public class GenerationController {

    private final GenerationService generationService;

    public GenerationController(GenerationService generationService) {
        this.generationService = generationService;
    }

    @PostMapping("/api/generations")
    public ApiResponse<GenerationCreateResponse> create(@RequestBody GenerationCreateRequest request) {
        return ApiResponse.success(generationService.create(request));
    }

    @GetMapping("/api/generations/{jobId}")
    public ApiResponse<GenerationStatusResponse> getStatus(@PathVariable String jobId) {
        return ApiResponse.success(generationService.getStatus(jobId));
    }

    @GetMapping("/api/generations/{jobId}/result")
    public ApiResponse<GenerationResultResponse> getResult(@PathVariable String jobId) {
        return ApiResponse.success(generationService.getResult(jobId));
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
