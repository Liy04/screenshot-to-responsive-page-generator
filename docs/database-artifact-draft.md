# Generation Artifact 数据库设计草案

## 重要声明

本文件仅为后续阶段数据库设计草案。

Week 03 不执行建表。

Week 03 不新增 Entity。

Week 03 不新增 Mapper。

Week 03 不进行 MySQL 实际落库。

## 草案背景

后续如果产品负责人确认进入数据库任务，可以考虑把生成任务产物拆成独立 artifact 表。

一个生成任务未来可能产生：

- `layout_json`
- `vue_code`
- `css_code`
- `preview_image`
- `export_zip`

## 表结构草案

```sql
CREATE TABLE generation_artifact (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    job_id BIGINT NOT NULL COMMENT '生成任务ID',
    artifact_type VARCHAR(50) NOT NULL COMMENT 'layout_json, vue_code, css_code, preview_image, export_zip',
    schema_version VARCHAR(20) COMMENT '产物结构版本，例如 0.1',
    content_json JSON COMMENT 'JSON 类型产物内容',
    content_text LONGTEXT COMMENT '代码类产物内容，例如 Vue/CSS',
    file_url VARCHAR(500) COMMENT '文件类产物地址',
    status VARCHAR(30) DEFAULT 'created' COMMENT 'created, validated, failed',
    error_message TEXT COMMENT '校验或生成失败原因',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY uk_job_artifact_type (job_id, artifact_type)
);
```

## 执行条件

只有在产品负责人明确确认进入数据库任务后，才允许：

- 评审表结构。
- 新增数据库迁移或初始化脚本。
- 新增 Entity / Mapper。
- 接入 MySQL 实际落库。
