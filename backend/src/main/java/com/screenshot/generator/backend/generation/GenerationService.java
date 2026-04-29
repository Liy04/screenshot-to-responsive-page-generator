package com.screenshot.generator.backend.generation;

import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.List;
import java.util.Map;
import java.util.UUID;
import java.util.concurrent.ConcurrentHashMap;

import com.screenshot.generator.backend.asset.AssetService;
import com.screenshot.generator.backend.common.ResourceNotFoundException;

import org.springframework.stereotype.Service;

@Service
public class GenerationService {

    private static final DateTimeFormatter DATE_TIME_FORMATTER = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss");
    private static final String SUPPORTED_MODE = "screenshot";
    private static final String SUPPORTED_TARGET_STACK = "vue3-css";
    private static final String SUCCESS_STATUS = "success";

    private final AssetService assetService;
    private final Map<String, GenerationJob> jobs = new ConcurrentHashMap<>();

    public GenerationService(AssetService assetService) {
        this.assetService = assetService;
    }

    public GenerationCreateResponse create(GenerationCreateRequest request) {
        validateCreateRequest(request);

        String jobId = "job_" + UUID.randomUUID().toString().replace("-", "");
        GenerationJob job = new GenerationJob(
                jobId,
                request.assetId(),
                request.mode(),
                request.targetStack(),
                request.responsive(),
                SUCCESS_STATUS,
                100,
                LocalDateTime.now().format(DATE_TIME_FORMATTER));
        jobs.put(jobId, job);

        return new GenerationCreateResponse(jobId, job.status());
    }

    public GenerationStatusResponse getStatus(String jobId) {
        GenerationJob job = getRequiredJob(jobId);
        return new GenerationStatusResponse(
                job.jobId(),
                job.assetId(),
                job.mode(),
                job.status(),
                job.progress(),
                job.createdAt());
    }

    public GenerationResultResponse getResult(String jobId) {
        GenerationJob job = getRequiredJob(jobId);
        return new GenerationResultResponse(
                job.jobId(),
                "artifact_" + job.jobId().substring("job_".length()),
                buildMockLayoutJson(),
                buildMockVueCode(),
                buildMockCssCode());
    }

    private void validateCreateRequest(GenerationCreateRequest request) {
        if (request == null) {
            throw new IllegalArgumentException("请求体不能为空");
        }

        if (isBlank(request.assetId())) {
            throw new IllegalArgumentException("assetId 不能为空");
        }

        if (!assetService.exists(request.assetId())) {
            throw new ResourceNotFoundException("资源不存在");
        }

        if (!SUPPORTED_MODE.equals(request.mode())) {
            throw new IllegalArgumentException("mode 仅支持 screenshot");
        }

        if (!SUPPORTED_TARGET_STACK.equals(request.targetStack())) {
            throw new IllegalArgumentException("targetStack 仅支持 vue3-css");
        }

        if (request.responsive() == null) {
            throw new IllegalArgumentException("responsive 不能为空");
        }
    }

    private GenerationJob getRequiredJob(String jobId) {
        GenerationJob job = jobs.get(jobId);
        if (job == null) {
            throw new ResourceNotFoundException("任务不存在");
        }
        return job;
    }

    private boolean isBlank(String value) {
        return value == null || value.isBlank();
    }

    private Map<String, Object> buildMockLayoutJson() {
        return Map.of(
                "pageName", "MockLandingPage",
                "layoutType", "landing",
                "sections", List.of(Map.of(
                        "id", "hero",
                        "type", "hero",
                        "title", "Mock 页面标题",
                        "description", "这是一个模拟生成结果",
                        "buttonText", "立即开始")));
    }

    private String buildMockVueCode() {
        return """
                <template>
                  <main class="generated-page">
                    <section class="hero-section">
                      <h1>Mock 页面标题</h1>
                      <p>这是一个模拟生成结果</p>
                      <button>立即开始</button>
                    </section>
                  </main>
                </template>""";
    }

    private String buildMockCssCode() {
        return """
                .generated-page { min-height: 100vh; }
                .hero-section { padding: 64px 24px; text-align: center; }""";
    }
}
