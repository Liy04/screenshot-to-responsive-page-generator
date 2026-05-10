package com.screenshot.generator.backend.layout;

import static org.hamcrest.Matchers.containsString;
import static org.hamcrest.Matchers.hasSize;
import static org.hamcrest.Matchers.is;
import static org.hamcrest.Matchers.isEmptyOrNullString;
import static org.hamcrest.Matchers.matchesPattern;
import static org.hamcrest.Matchers.not;
import static org.hamcrest.Matchers.nullValue;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.MvcResult;

@SpringBootTest
@AutoConfigureMockMvc
class ImagePageJobControllerTest {

    private static final String JOBS_PATH = "/api/dev/image-page-jobs";
    private static final String JOB_PATH = "/api/dev/image-page-jobs/{jobId}";

    @Autowired
    private MockMvc mockMvc;

    @Test
    void createLandingBasicPageJobReturnsSuccessApiResponse() throws Exception {
        mockMvc.perform(post(JOBS_PATH)
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(requestBody("demo-home.png", "landing-basic")))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.code", is(200)))
                .andExpect(jsonPath("$.message", is("success")))
                .andExpect(jsonPath("$.data.jobId", matchesPattern("img-page-\\d{3}")))
                .andExpect(jsonPath("$.data.status", is("SUCCESS")))
                .andExpect(jsonPath("$.data.sourceType", is("IMAGE_TEMPLATE_MOCK")))
                .andExpect(jsonPath("$.data.imageName", is("demo-home.png")))
                .andExpect(jsonPath("$.data.templateKey", is("landing-basic")))
                .andExpect(jsonPath("$.data.layoutArtifact.status", is("SUCCESS")))
                .andExpect(jsonPath("$.data.layoutArtifact.layoutJson.version", is("0.1")))
                .andExpect(jsonPath("$.data.layoutArtifact.layoutJson.layout").exists())
                .andExpect(jsonPath("$.data.generatedPageArtifact.status", is("SUCCESS")))
                .andExpect(jsonPath("$.data.generatedPageArtifact.htmlCode", not(isEmptyOrNullString())))
                .andExpect(jsonPath("$.data.generatedPageArtifact.cssCode", not(isEmptyOrNullString())))
                .andExpect(jsonPath("$.data.generatedPageArtifact.vueCode", not(isEmptyOrNullString())))
                .andExpect(jsonPath("$.data.errors", hasSize(0)))
                .andExpect(jsonPath("$.data.generatedPageArtifact.htmlCode", not(containsString("<script"))))
                .andExpect(jsonPath("$.data.generatedPageArtifact.htmlCode", not(containsString("onclick"))))
                .andExpect(jsonPath("$.data.generatedPageArtifact.htmlCode", not(containsString("onerror"))))
                .andExpect(jsonPath("$.data.generatedPageArtifact.htmlCode", not(containsString("onload"))))
                .andExpect(jsonPath("$.data.generatedPageArtifact.htmlCode", not(containsString("javascript:"))));
    }

    @Test
    void createCardListPageJobReturnsSuccessApiResponse() throws Exception {
        mockMvc.perform(post(JOBS_PATH)
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(requestBody("cards.png", "card-list")))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.code", is(200)))
                .andExpect(jsonPath("$.data.status", is("SUCCESS")))
                .andExpect(jsonPath("$.data.templateKey", is("card-list")))
                .andExpect(jsonPath("$.data.layoutArtifact.status", is("SUCCESS")))
                .andExpect(jsonPath("$.data.generatedPageArtifact.status", is("SUCCESS")))
                .andExpect(jsonPath("$.data.generatedPageArtifact.htmlCode", not(isEmptyOrNullString())))
                .andExpect(jsonPath("$.data.generatedPageArtifact.cssCode", not(isEmptyOrNullString())))
                .andExpect(jsonPath("$.data.generatedPageArtifact.vueCode", not(isEmptyOrNullString())));
    }

    @Test
    void createInvalidLayoutPageJobReturnsFailedDataInSuccessApiResponse() throws Exception {
        mockMvc.perform(post(JOBS_PATH)
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(requestBody("broken.png", "invalid-layout")))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.code", is(200)))
                .andExpect(jsonPath("$.message", is("success")))
                .andExpect(jsonPath("$.data.status", is("FAILED")))
                .andExpect(jsonPath("$.data.layoutArtifact.status", is("FAILED")))
                .andExpect(jsonPath("$.data.generatedPageArtifact").value(nullValue()))
                .andExpect(jsonPath("$.data.errors", hasSize(1)))
                .andExpect(jsonPath("$.data.errors[0].code", is("INVALID_LAYOUT_TEMPLATE")));
    }

    @Test
    void createPageJobReturnsBadRequestForUnknownTemplateKey() throws Exception {
        mockMvc.perform(post(JOBS_PATH)
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(requestBody("demo-home.png", "unknown-template")))
                .andExpect(status().isBadRequest())
                .andExpect(jsonPath("$.code", is(400)))
                .andExpect(jsonPath("$.message", containsString("Unknown templateKey")))
                .andExpect(jsonPath("$.data").doesNotExist());
    }

    @Test
    void getExistingPageJobReturnsCreatedJob() throws Exception {
        MvcResult createResult = mockMvc.perform(post(JOBS_PATH)
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(requestBody("query-page.png", "landing-basic")))
                .andExpect(status().isOk())
                .andReturn();
        String responseBody = createResult.getResponse().getContentAsString();
        String jobId = responseBody.replaceFirst("(?s).*\"jobId\"\\s*:\\s*\"([^\"]+)\".*", "$1");

        mockMvc.perform(get(JOB_PATH, jobId))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.code", is(200)))
                .andExpect(jsonPath("$.data.jobId", is(jobId)))
                .andExpect(jsonPath("$.data.status", is("SUCCESS")))
                .andExpect(jsonPath("$.data.generatedPageArtifact.status", is("SUCCESS")))
                .andExpect(jsonPath("$.data.generatedPageArtifact.htmlCode", not(isEmptyOrNullString())));
    }

    @Test
    void getMissingPageJobReturnsNotFoundApiResponse() throws Exception {
        mockMvc.perform(get(JOB_PATH, "img-page-not-found"))
                .andExpect(status().isNotFound())
                .andExpect(jsonPath("$.code", is(404)))
                .andExpect(jsonPath("$.message", is("image-page job 不存在")))
                .andExpect(jsonPath("$.data").doesNotExist());
    }

    @Test
    void createPageJobReturnsBadRequestWhenImageNameIsBlank() throws Exception {
        mockMvc.perform(post(JOBS_PATH)
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(requestBody(" ", "landing-basic")))
                .andExpect(status().isBadRequest())
                .andExpect(jsonPath("$.code", is(400)))
                .andExpect(jsonPath("$.message", is("imageName 不能为空")))
                .andExpect(jsonPath("$.data").doesNotExist());
    }

    @Test
    void createPageJobReturnsBadRequestWhenTemplateKeyIsBlank() throws Exception {
        mockMvc.perform(post(JOBS_PATH)
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(requestBody("demo-home.png", " ")))
                .andExpect(status().isBadRequest())
                .andExpect(jsonPath("$.code", is(400)))
                .andExpect(jsonPath("$.message", is("templateKey 不能为空")))
                .andExpect(jsonPath("$.data").doesNotExist());
    }

    @Test
    void createPageJobReturnsBadRequestWhenBodyIsEmpty() throws Exception {
        mockMvc.perform(post(JOBS_PATH)
                        .contentType(MediaType.APPLICATION_JSON))
                .andExpect(status().isBadRequest())
                .andExpect(jsonPath("$.code", is(400)))
                .andExpect(jsonPath("$.message", is("请求体不能为空")))
                .andExpect(jsonPath("$.data").doesNotExist());
    }

    @Test
    void createPageJobReturnsBadRequestWhenBodyIsArray() throws Exception {
        mockMvc.perform(post(JOBS_PATH)
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("[]"))
                .andExpect(status().isBadRequest())
                .andExpect(jsonPath("$.code", is(400)))
                .andExpect(jsonPath("$.message", is("请求体必须是 JSON 对象")))
                .andExpect(jsonPath("$.data").doesNotExist());
    }

    private static String requestBody(String imageName, String templateKey) {
        return """
                {
                  "imageName": "%s",
                  "templateKey": "%s"
                }
                """.formatted(imageName, templateKey);
    }
}
