package com.screenshot.generator.backend.layout;

import static org.hamcrest.Matchers.is;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.put;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.List;

import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;

@SpringBootTest
@AutoConfigureMockMvc
class GeneratedPageArtifactControllerTest {

    private static final String BASE_PATH = "/api/dev/generation-jobs/{jobId}/artifacts/generated-page";
    private static final Path GENERATED_PAGE_STORAGE_DIRECTORY = Path.of(
            "mock-data",
            "generated-page-artifacts").toAbsolutePath().normalize();
    private static final List<String> TEST_JOB_IDS = List.of(
            "test_day5_generated_page_success",
            "test_day5_generated_page_failed",
            "test_day5_generated_page_large",
            "test_day5_generated_page_missing");

    @Autowired
    private MockMvc mockMvc;

    @BeforeEach
    void cleanBeforeEach() throws IOException {
        cleanTestArtifacts();
    }

    @AfterEach
    void cleanAfterEach() throws IOException {
        cleanTestArtifacts();
    }

    @Test
    void saveGeneratedPageArtifactReturnsSuccess() throws Exception {
        String jobId = "test_day5_generated_page_success";

        mockMvc.perform(put(BASE_PATH, jobId)
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(successArtifact(jobId)))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.code", is(200)))
                .andExpect(jsonPath("$.message", is("success")))
                .andExpect(jsonPath("$.data.jobId", is(jobId)))
                .andExpect(jsonPath("$.data.artifactType", is("generated-page")))
                .andExpect(jsonPath("$.data.mockPath", is(
                        "mock-data/generated-page-artifacts/" + jobId + ".generated-page.json")))
                .andExpect(jsonPath("$.data.status", is("SUCCESS")));
    }

    @Test
    void getGeneratedPageArtifactReturnsSavedArtifact() throws Exception {
        String jobId = "test_day5_generated_page_success";

        mockMvc.perform(put(BASE_PATH, jobId)
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(successArtifact(jobId)))
                .andExpect(status().isOk());

        mockMvc.perform(get(BASE_PATH, jobId))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.code", is(200)))
                .andExpect(jsonPath("$.message", is("success")))
                .andExpect(jsonPath("$.data.jobId", is(jobId)))
                .andExpect(jsonPath("$.data.artifactType", is("generated-page")))
                .andExpect(jsonPath("$.data.status", is("SUCCESS")))
                .andExpect(jsonPath("$.data.htmlCode", is("<section class=\"lg-section\"><h1>Preview</h1></section>")))
                .andExpect(jsonPath("$.data.cssCode", is(".lg-section { padding: 24px; }")))
                .andExpect(jsonPath("$.data.validation.passed", is(true)));
    }

    @Test
    void getGeneratedPageArtifactReturnsNotFoundWhenArtifactDoesNotExist() throws Exception {
        mockMvc.perform(get(BASE_PATH, "test_day5_generated_page_missing"))
                .andExpect(status().isNotFound())
                .andExpect(jsonPath("$.code", is(404)))
                .andExpect(jsonPath("$.message", is("generated-page artifact 不存在")))
                .andExpect(jsonPath("$.data").doesNotExist());
    }

    @Test
    void generatedPageArtifactReturnsBadRequestForInvalidJobId() throws Exception {
        String invalidJobId = "bad..id";

        mockMvc.perform(get(BASE_PATH, invalidJobId))
                .andExpect(status().isBadRequest())
                .andExpect(jsonPath("$.code", is(400)))
                .andExpect(jsonPath("$.message", is("jobId 格式不合法")))
                .andExpect(jsonPath("$.data").doesNotExist());

        mockMvc.perform(put(BASE_PATH, invalidJobId)
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(successArtifact("test_day5_generated_page_success")))
                .andExpect(status().isBadRequest())
                .andExpect(jsonPath("$.code", is(400)))
                .andExpect(jsonPath("$.message", is("jobId 格式不合法")))
                .andExpect(jsonPath("$.data").doesNotExist());
    }

    @Test
    void saveGeneratedPageArtifactReturnsBadRequestWhenPayloadExceedsTwoMegabytes() throws Exception {
        String jobId = "test_day5_generated_page_large";

        mockMvc.perform(put(BASE_PATH, jobId)
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(largeArtifact(jobId)))
                .andExpect(status().isBadRequest())
                .andExpect(jsonPath("$.code", is(400)))
                .andExpect(jsonPath("$.message", is("generated-page artifact 不能超过 2MB")))
                .andExpect(jsonPath("$.data").doesNotExist());
    }

    @Test
    void saveAndGetFailedGeneratedPageArtifact() throws Exception {
        String jobId = "test_day5_generated_page_failed";

        mockMvc.perform(put(BASE_PATH, jobId)
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(failedArtifact(jobId)))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.data.status", is("FAILED")));

        mockMvc.perform(get(BASE_PATH, jobId))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.code", is(200)))
                .andExpect(jsonPath("$.data.jobId", is(jobId)))
                .andExpect(jsonPath("$.data.status", is("FAILED")))
                .andExpect(jsonPath("$.data.validation.passed", is(false)))
                .andExpect(jsonPath("$.data.validation.errors[0].code", is("LAYOUT_INVALID")))
                .andExpect(jsonPath("$.data.htmlCode", is("")))
                .andExpect(jsonPath("$.data.cssCode", is("")))
                .andExpect(jsonPath("$.data.vueCode", is("")));
    }

    private static String successArtifact(String jobId) {
        return """
                {
                  "version": "0.1",
                  "artifactType": "generated-page",
                  "jobId": "%s",
                  "generator": {
                    "name": "layout-static-generator",
                    "version": "0.1"
                  },
                  "source": {
                    "layoutVersion": "0.1",
                    "layoutHash": "test-layout-hash",
                    "layoutSourceType": "manual"
                  },
                  "validation": {
                    "passed": true,
                    "errors": [],
                    "warnings": []
                  },
                  "status": "SUCCESS",
                  "htmlCode": "<section class=\\"lg-section\\"><h1>Preview</h1></section>",
                  "cssCode": ".lg-section { padding: 24px; }",
                  "vueCode": "<template><section class=\\"lg-section\\"><h1>Preview</h1></section></template>",
                  "unsupportedNodes": [],
                  "createdAt": "2026-05-08T10:00:00+08:00"
                }
                """.formatted(jobId);
    }

    private static String failedArtifact(String jobId) {
        return """
                {
                  "version": "0.1",
                  "artifactType": "generated-page",
                  "jobId": "%s",
                  "generator": {
                    "name": "layout-static-generator",
                    "version": "0.1"
                  },
                  "source": {
                    "layoutVersion": "0.1",
                    "layoutHash": "failed-layout-hash",
                    "layoutSourceType": "manual"
                  },
                  "validation": {
                    "passed": false,
                    "errors": [
                      {
                        "code": "LAYOUT_INVALID",
                        "message": "layout is invalid",
                        "path": "layout"
                      }
                    ],
                    "warnings": []
                  },
                  "status": "FAILED",
                  "htmlCode": "",
                  "cssCode": "",
                  "vueCode": "",
                  "unsupportedNodes": [],
                  "createdAt": "2026-05-08T10:00:00+08:00"
                }
                """.formatted(jobId);
    }

    private static String largeArtifact(String jobId) {
        String htmlCode = "x".repeat(2 * 1024 * 1024);
        return """
                {
                  "version": "0.1",
                  "artifactType": "generated-page",
                  "jobId": "%s",
                  "generator": {
                    "name": "layout-static-generator",
                    "version": "0.1"
                  },
                  "source": {
                    "layoutVersion": "0.1",
                    "layoutHash": "large-layout-hash",
                    "layoutSourceType": "manual"
                  },
                  "validation": {
                    "passed": true,
                    "errors": [],
                    "warnings": []
                  },
                  "status": "SUCCESS",
                  "htmlCode": "%s",
                  "cssCode": ".lg-section { padding: 24px; }",
                  "vueCode": "",
                  "unsupportedNodes": [],
                  "createdAt": "2026-05-08T10:00:00+08:00"
                }
                """.formatted(jobId, htmlCode);
    }

    private static void cleanTestArtifacts() throws IOException {
        for (String jobId : TEST_JOB_IDS) {
            Files.deleteIfExists(GENERATED_PAGE_STORAGE_DIRECTORY.resolve(jobId + ".generated-page.json"));
        }
    }
}
