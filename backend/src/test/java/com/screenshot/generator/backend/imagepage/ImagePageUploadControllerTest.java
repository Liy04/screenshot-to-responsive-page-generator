package com.screenshot.generator.backend.imagepage;

import static org.hamcrest.Matchers.containsString;
import static org.hamcrest.Matchers.is;
import static org.hamcrest.Matchers.matchesPattern;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.multipart;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.content;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.header;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.http.MediaType;
import org.springframework.mock.web.MockMultipartFile;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.MvcResult;

@SpringBootTest
@AutoConfigureMockMvc
class ImagePageUploadControllerTest {

    private static final String UPLOAD_PATH = "/api/image-page/upload";
    private static final String SOURCE_PATH = "/api/image-page/jobs/{jobId}/source";
    private static final String GENERATE_PATH = "/api/image-page/jobs/{jobId}/generate";

    @Autowired
    private MockMvc mockMvc;

    @Test
    void uploadPngReturnsJobIdFileNameAndSourceUrl() throws Exception {
        MockMultipartFile file = new MockMultipartFile(
                "file",
                "demo-home.png",
                "image/png",
                "png-content".getBytes());

        mockMvc.perform(multipart(UPLOAD_PATH).file(file))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.code", is(200)))
                .andExpect(jsonPath("$.message", is("upload success")))
                .andExpect(jsonPath("$.data.jobId", matchesPattern("imgjob_[A-Za-z0-9]{32}")))
                .andExpect(jsonPath("$.data.fileName", is("demo-home.png")))
                .andExpect(jsonPath("$.data.sourceUrl", containsString("/api/image-page/jobs/")))
                .andExpect(jsonPath("$.data.imagePath").doesNotExist());
    }

    @Test
    void uploadJpegReturnsSourceUrl() throws Exception {
        MockMultipartFile file = new MockMultipartFile(
                "file",
                "photo.jpg",
                "image/jpeg",
                "jpeg-content".getBytes());

        mockMvc.perform(multipart(UPLOAD_PATH).file(file))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.code", is(200)))
                .andExpect(jsonPath("$.data.fileName", is("photo.jpg")))
                .andExpect(jsonPath("$.data.sourceUrl", containsString("/api/image-page/jobs/")));
    }

    @Test
    void uploadWebpReturnsSourceUrl() throws Exception {
        MockMultipartFile file = new MockMultipartFile(
                "file",
                "preview.webp",
                "image/webp",
                "webp-content".getBytes());

        mockMvc.perform(multipart(UPLOAD_PATH).file(file))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.code", is(200)))
                .andExpect(jsonPath("$.data.fileName", is("preview.webp")))
                .andExpect(jsonPath("$.data.sourceUrl", containsString("/api/image-page/jobs/")));
    }

    @Test
    void uploadRejectsNonImageFile() throws Exception {
        MockMultipartFile file = new MockMultipartFile(
                "file",
                "note.txt",
                MediaType.TEXT_PLAIN_VALUE,
                "plain text".getBytes());

        mockMvc.perform(multipart(UPLOAD_PATH).file(file))
                .andExpect(status().isBadRequest())
                .andExpect(jsonPath("$.code", is(400)))
                .andExpect(jsonPath("$.message", is("只支持 PNG、JPG、JPEG、WebP 图片")))
                .andExpect(jsonPath("$.data").doesNotExist());
    }

    @Test
    void uploadRejectsMultipleFiles() throws Exception {
        MockMultipartFile first = new MockMultipartFile(
                "file",
                "first.png",
                "image/png",
                "first".getBytes());
        MockMultipartFile second = new MockMultipartFile(
                "file",
                "second.png",
                "image/png",
                "second".getBytes());

        mockMvc.perform(multipart(UPLOAD_PATH).file(first).file(second))
                .andExpect(status().isBadRequest())
                .andExpect(jsonPath("$.code", is(400)))
                .andExpect(jsonPath("$.message", is("只支持单张图片上传")))
                .andExpect(jsonPath("$.data").doesNotExist());
    }

    @Test
    void uploadRejectsOversizedFile() throws Exception {
        byte[] oversized = new byte[5 * 1024 * 1024 + 1];
        MockMultipartFile file = new MockMultipartFile(
                "file",
                "huge.png",
                "image/png",
                oversized);

        mockMvc.perform(multipart(UPLOAD_PATH).file(file))
                .andExpect(status().isBadRequest())
                .andExpect(jsonPath("$.code", is(400)))
                .andExpect(jsonPath("$.message", is("上传文件不能超过 5MB")))
                .andExpect(jsonPath("$.data").doesNotExist());
    }

    @Test
    void sourceUrlReturnsOriginalPngBytes() throws Exception {
        byte[] payload = "source-bytes".getBytes();
        MockMultipartFile file = new MockMultipartFile(
                "file",
                "origin.png",
                "image/png",
                payload);

        MvcResult uploadResult = mockMvc.perform(multipart(UPLOAD_PATH).file(file))
                .andExpect(status().isOk())
                .andReturn();
        String responseBody = uploadResult.getResponse().getContentAsString();
        String jobId = responseBody.replaceFirst("(?s).*\"jobId\"\\s*:\\s*\"([^\"]+)\".*", "$1");

        mockMvc.perform(get(SOURCE_PATH, jobId))
                .andExpect(status().isOk())
                .andExpect(content().contentType("image/png"))
                .andExpect(header().string("Content-Disposition", containsString("origin.png")))
                .andExpect(content().bytes(payload));
    }

    @Test
    void sourceUrlReturnsNotFoundForMissingJob() throws Exception {
        mockMvc.perform(get(SOURCE_PATH, "imgjob_missing"))
                .andExpect(status().isNotFound())
                .andExpect(jsonPath("$.code", is(404)))
                .andExpect(jsonPath("$.message", is("原图不存在")))
                .andExpect(jsonPath("$.data").doesNotExist());
    }

    @Test
    void sourceUrlRejectsIllegalJobId() throws Exception {
        mockMvc.perform(get(SOURCE_PATH, "bad..id"))
                .andExpect(status().isBadRequest())
                .andExpect(jsonPath("$.code", is(400)))
                .andExpect(jsonPath("$.message", is("jobId 格式不合法")))
                .andExpect(jsonPath("$.data").doesNotExist());
    }

    @Test
    void generateInvokesPythonWorkerAfterUpload() throws Exception {
        MockMultipartFile file = new MockMultipartFile(
                "file",
                "generate.png",
                "image/png",
                "generate-content".getBytes());

        MvcResult uploadResult = mockMvc.perform(multipart(UPLOAD_PATH).file(file))
                .andExpect(status().isOk())
                .andReturn();
        String responseBody = uploadResult.getResponse().getContentAsString();
        String jobId = responseBody.replaceFirst("(?s).*\"jobId\"\\s*:\\s*\"([^\"]+)\".*", "$1");

        mockMvc.perform(post(GENERATE_PATH, jobId))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.code", is(200)))
                .andExpect(jsonPath("$.data.jobId", is(jobId)))
                .andExpect(jsonPath("$.data.status", is("SUCCESS")))
                .andExpect(jsonPath("$.data.mode", is("real-ai")))
                .andExpect(jsonPath("$.data.fallbackUsed").exists())
                .andExpect(jsonPath("$.data.sourceType", matchesPattern(".+")))
                .andExpect(jsonPath("$.data.exitCode", is(0)))
                .andExpect(jsonPath("$.data.layoutJson.version", is("0.1")))
                .andExpect(jsonPath("$.data.layoutJson.layout").exists())
                .andExpect(jsonPath("$.data.previewHtml", containsString("<!doctype html>")))
                .andExpect(jsonPath("$.data.validation.ok", is(true)))
                .andExpect(jsonPath("$.data.message", matchesPattern(".+")))
                .andExpect(jsonPath("$.data.stdout", containsString(jobId)))
                .andExpect(jsonPath("$.data.layoutJson.imagePath").doesNotExist());
    }

    @Test
    void generateReturnsNotFoundWhenSourceIsMissing() throws Exception {
        mockMvc.perform(post(GENERATE_PATH, "imgjob_missing"))
                .andExpect(status().isNotFound())
                .andExpect(jsonPath("$.code", is(404)))
                .andExpect(jsonPath("$.message", is("原图不存在")))
                .andExpect(jsonPath("$.data").doesNotExist());
    }

    @Test
    void generateRejectsIllegalJobId() throws Exception {
        mockMvc.perform(post(GENERATE_PATH, "bad..id"))
                .andExpect(status().isBadRequest())
                .andExpect(jsonPath("$.code", is(400)))
                .andExpect(jsonPath("$.message", is("jobId 格式不合法")))
                .andExpect(jsonPath("$.data").doesNotExist());
    }
}
