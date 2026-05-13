package com.screenshot.generator.backend.imagepage;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.mock.web.MockMultipartFile;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.MvcResult;

import static org.hamcrest.Matchers.containsString;
import static org.hamcrest.Matchers.is;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.multipart;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

@SpringBootTest(properties = "imagepage.worker.mode=broken-mode")
@AutoConfigureMockMvc
class ImagePageGenerateWorkerFailureControllerTest {

    private static final String UPLOAD_PATH = "/api/image-page/upload";
    private static final String GENERATE_PATH = "/api/image-page/jobs/{jobId}/generate";

    @Autowired
    private MockMvc mockMvc;

    @Test
    void generateReturnsClearErrorWhenWorkerExitsNonZero() throws Exception {
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

        mockMvc.perform(post(GENERATE_PATH, jobId))
                .andExpect(status().isInternalServerError())
                .andExpect(jsonPath("$.code", is(500)))
                .andExpect(jsonPath("$.message", containsString("exitCode=")))
                .andExpect(jsonPath("$.data").doesNotExist());
    }
}
