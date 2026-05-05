# ADR-0001: 默认技术栈

## 状态

Accepted

## 背景

项目需要保持前端、后端和 Worker 的协作边界清晰，避免每个阶段反复讨论基础技术选型。

## 决策

默认技术栈如下：

- 前端：Vue3 + Vite + JavaScript
- 后端：Java 17 + Spring Boot + Maven
- 数据库：MySQL，作为长期方向
- 数据访问：MyBatis-Plus，作为长期方向
- Worker：Python 3.11 推荐目标版本
- 测试：smoke test、接口测试、前端页面测试

除非用户或项目经理明确确认，不擅自替换技术栈。

## 影响

- 当前阶段可以继续使用 mock、标准库脚本和轻量验证。
- MySQL / MyBatis-Plus 是长期方向，不代表当前阶段必须实际落库。
- 新增依赖或替换框架前必须先说明原因并等待确认。

