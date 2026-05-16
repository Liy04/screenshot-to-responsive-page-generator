package com.screenshot.generator.backend.imagepage;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.AfterEach;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.mock.web.MockMultipartFile;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.MvcResult;

import java.nio.file.Path;
import java.nio.file.Files;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;

import static org.hamcrest.Matchers.containsString;
import static org.hamcrest.Matchers.is;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.anyBoolean;
import static org.mockito.ArgumentMatchers.anyString;
import static org.mockito.Mockito.when;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.multipart;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

@SpringBootTest
@AutoConfigureMockMvc
class ImagePageGenerateWorkerFailureControllerTest {

    private static final String UPLOAD_PATH = "/api/image-page/upload";
    private static final String GENERATE_PATH = "/api/image-page/jobs/{jobId}/generate";

    @Autowired
    private MockMvc mockMvc;

    @MockBean
    private ImagePageWorkerRunner workerRunner;

    private final List<String> createdJobIds = new ArrayList<>();

    @AfterEach
    void cleanupCreatedJobDirectories() throws IOException {
        for (String jobId : createdJobIds) {
            Path jobDirectory = Path.of("storage", "temp", jobId).toAbsolutePath().normalize();
            if (!Files.exists(jobDirectory)) {
                continue;
            }
            try (var pathStream = Files.walk(jobDirectory)) {
                pathStream.sorted(Comparator.reverseOrder())
                        .forEach(path -> {
                            try {
                                Files.deleteIfExists(path);
                            } catch (IOException ignored) {
                            }
                        });
            }
        }
        createdJobIds.clear();
    }

    @Test
    void generateReturnsClearErrorWhenWorkerExitsNonZero() throws Exception {
        when(workerRunner.run(anyString(), any(Path.class), anyString(), anyString(), anyString(), anyBoolean(), any(), any(Path.class)))
                .thenReturn(new ImagePageWorkerExecutionResult(2, "", "mock worker failed"));

        MockMultipartFile file = new MockMultipartFile(
                "file",
                "broken-mode.png",
                "image/png",
                "broken-mode-content".getBytes());

        MvcResult uploadResult = mockMvc.perform(multipart(UPLOAD_PATH).file(file))
                .andExpect(status().isOk())
                .andReturn();
        String responseBody = uploadResult.getResponse().getContentAsString();
        String jobId = responseBody.replaceFirst("(?s).*\"jobId\"\\s*:\\s*\"([^\"]+)\".*", "$1");
        createdJobIds.add(jobId);

        mockMvc.perform(post(GENERATE_PATH, jobId))
                .andExpect(status().isInternalServerError())
                .andExpect(jsonPath("$.code", is(500)))
                .andExpect(jsonPath("$.message", containsString("exitCode=")))
                .andExpect(jsonPath("$.data").doesNotExist());
    }

    @Test
    void generateReturnsGatewayTimeoutWhenWorkerTimesOut() throws Exception {
        when(workerRunner.run(anyString(), any(Path.class), anyString(), anyString(), anyString(), anyBoolean(), any(), any(Path.class)))
                .thenThrow(new ImagePageWorkerTimeoutException("Python Worker 执行超时，超过 30 秒"));

        MockMultipartFile file = new MockMultipartFile(
                "file",
                "timeout.png",
                "image/png",
                "timeout-content".getBytes());

        MvcResult uploadResult = mockMvc.perform(multipart(UPLOAD_PATH).file(file))
                .andExpect(status().isOk())
                .andReturn();
        String responseBody = uploadResult.getResponse().getContentAsString();
        String jobId = responseBody.replaceFirst("(?s).*\"jobId\"\\s*:\\s*\"([^\"]+)\".*", "$1");
        createdJobIds.add(jobId);

        mockMvc.perform(post(GENERATE_PATH, jobId))
                .andExpect(status().isGatewayTimeout())
                .andExpect(jsonPath("$.code", is(504)))
                .andExpect(jsonPath("$.message", containsString("超时")))
                .andExpect(jsonPath("$.data").doesNotExist());
    }
}
