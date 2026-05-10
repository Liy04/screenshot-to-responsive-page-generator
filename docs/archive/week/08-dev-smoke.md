# Week 08 Dev Smoke

## Environment

- Backend: 8080
- Frontend: 5174
- Worker: not started
- MySQL: not used
- Redis: not used
- RabbitMQ: not used
- AI: not used
- Figma: not used

## Cases

### landing-basic

Result: PASS
Notes: 返回 `SUCCESS`，展示 Layout JSON、generatedPageArtifact 和 iframe 预览。

### card-list

Result: PASS
Notes: 返回 `SUCCESS`，展示 Layout JSON、generatedPageArtifact 和 iframe 预览。

### invalid-layout

Result: PASS
Notes: 返回 `200 + FAILED`，不展示 iframe，展示 errors。

### unknown-template

Result: PASS
Notes: 返回 `400`，不返回 SUCCESS。

### nonexistent jobId

Result: PASS
Notes: 返回 `404`，不返回伪造 job。

## Security Check

- iframe sandbox="": PASS
- no allow-scripts: PASS
- no real image upload: PASS
- no backend Python Worker call: PASS

## Final Result

Week 08 smoke result: PASS

## Day 7A / smoke 记录

- Worker 全量相关测试通过：45 tests OK。
- 后端测试通过：20 tests, 0 failures。
- 前端构建通过：`npm run build`。
- 前端测试通过：4 tests passed。
- 后端 jar 启动成功，8080 可用。
- 前端 dev server 启动成功，5174 可访问。
- `/dev/image-to-layout` 页面入口返回 200。
- Vite proxy 调 `/api/dev/image-page-jobs` 成功。
- `landing-basic` 返回 SUCCESS。
- `card-list` 返回 SUCCESS。
- `invalid-layout` 返回 200 且 FAILED。
- `unknown-template` 返回 400。
- 不存在 `jobId` 返回 404。
- iframe 使用 `sandbox=""`。
- 未发现运行时代码包含 `allow-scripts`。
- 后台 8080 / 5174 服务已停止。
- 未做 Playwright 视觉回归，符合边界。
