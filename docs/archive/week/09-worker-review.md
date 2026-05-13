# Worker 代码审查报告

> 审查日期：2026-05-11
> 审查范围：`worker/` 目录全部 Python 源码 + 目录结构

---

## 一、目录结构问题

### 当前结构

```
worker/
├── main.py
├── image_layout_pipeline.py         # 549 行
├── image_layout_resolver.py
├── layout_static_generator.py       # 542 行
├── layout_validator.py              # 433 行
├── real_ai_layout_client.py
├── test_*.py × 5                    # 散落在根目录
└── fixtures/image_templates/
```

### 问题清单

| # | 问题 | 严重度 | 说明 |
|---|------|--------|------|
| 1 | 测试文件与源码同级 | 中 | `test_*.py` 应放入 `tests/` 子目录 |
| 2 | 缺少 `__init__.py` | 中 | 导致每个文件都用 `try: from . import ... except ImportError: from ... import ...` 双路径 import |
| 3 | 缺少 `requirements.txt` / `pyproject.toml` | 中 | 外部依赖 `openai` 未 pin 版本，新人无法复现环境 |
| 4 | 缺少 pytest 配置 | 低 | 没有声明测试运行方式 |
| 5 | fixtures 与测试未关联 | 低 | 没有 `conftest.py` 统一管理 fixture 路径 |

### 推荐目标结构

```
worker/
├── pyproject.toml                   # 依赖 + pytest 配置
├── src/
│   └── worker/
│       ├── __init__.py
│       ├── main.py
│       ├── pipeline.py              # 去掉 image_layout_ 前缀
│       ├── resolver.py
│       ├── static_generator.py
│       ├── validator.py
│       └── ai_client.py
├── tests/
│   ├── conftest.py                  # fixture 路径统一管理
│   ├── fixtures/
│   │   └── image_templates/
│   │       ├── card-list.layout.json
│   │       ├── invalid-layout.layout.json
│   │       └── landing-basic.layout.json
│   ├── test_pipeline.py
│   ├── test_resolver.py
│   ├── test_static_generator.py
│   ├── test_validator.py
│   └── test_ai_client.py
└── README.md
```

---

## 二、跨模块重复代码

| 重复代码 | 出现位置 | 建议 |
|----------|----------|------|
| `message_to_dict()` | pipeline.py, generator.py | 提取到 `common.py` |
| `make_message()` | pipeline.py, generator.py | 同上 |
| `configure_output_encoding()` | validator.py，被 main.py/generator.py 导入 | 同上 |
| `try: from .X except: from X` | 所有文件 | 加 `__init__.py` 后统一删除 |
| result 构造函数（10 个参数） | pipeline.py × 3 处 | 用 dataclass 替代 |
| validate → repair → compile 流程 | pipeline.py × 2 处 | 抽取 `_finalize_layout()` |

### 建议新建 `common.py`

```python
from dataclasses import dataclass

@dataclass
class ValidationMessage:
    code: str
    message: str
    path: str

def message_to_dict(message: ValidationMessage) -> dict[str, str]:
    return {"code": message.code, "message": message.message, "path": message.path}

def make_message(code: str, message: str, path: str = "$") -> ValidationMessage:
    return ValidationMessage(code=code, message=message, path=path)

def configure_output_encoding() -> None:
    import sys
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")
```

---

## 三、逐模块代码问题

### 3.1 `layout_validator.py` — 最优雅，评分 8/10

**优点：**
- `ValidationMessage` / `ValidationResult` dataclass 建模清晰
- 递归 schema 校验 + 业务规则校验分离
- 纯函数、无副作用

**待改进：**
- `configure_output_encoding()` 不属于校验器职责，应移入 `common.py`
- 错误信息中英混杂：`"text 节点必须有 content"` vs 英文 error code，风格应统一

---

### 3.2 `layout_static_generator.py` — 功能完整但偏长，评分 7/10

**优点：**
- 安全白名单设计好（CSS 值白名单、FORBIDDEN_HTML_SNIPPETS、`is_safe_image_src()`）
- `compile_node()` 递归逻辑清晰
- `enforce_preview_html_safety()` 二次防御

**待改进：**

**542 行太长。** `compile_node()` 同时负责 HTML 生成 + CSS 收集 + 警告收集 + 不支持节点记录，建议拆出 `CompilerContext`：

```python
@dataclass
class CompilerContext:
    css_blocks: list[str]
    warnings: list[ValidationMessage]
    unsupported_nodes: list[dict[str, str]]
```

**`safe_css_value()` 是 40 行 if-elif 链，** 可用字典映射简化：

```python
CSS_VALIDATORS: dict[str, Callable[[str], bool]] = {
    "backgroundColor": is_safe_color,
    "color": is_safe_color,
    "width": is_safe_length,
    "height": is_safe_length,
    # ...
}

def safe_css_value(key: str, value: Any) -> str | None:
    # 数值处理 ...
    validator = CSS_VALIDATORS.get(key)
    if validator and validator(stripped):
        return stripped
    return None
```

---

### 3.3 `image_layout_pipeline.py` — 重复最多，评分 6/10

**核心问题：** `process_image_layout_job()` 里 fallback-only 和 real-ai 两条路径有大量重复。

**问题 1：10 参数函数**

`make_result()` 参数过多，可读性差。建议用 dataclass：

```python
@dataclass
class PipelineResult:
    job_id: str
    status: str
    mode: str
    fallback_used: bool
    source_type: str
    layout_json: dict | None
    errors: list[ValidationMessage]
    warnings: list[ValidationMessage]
    message: str
    preview_html: str = ""
```

**问题 2：重复的 finalize 流程**

两处几乎相同的 validate → repair → compile → make_result 逻辑，应抽取：

```python
def _finalize_layout(
    layout_json: dict[str, Any],
    image_name: str,
    job_id: str,
    mode: str,
    source_type: str,
    fallback_used: bool,
    extra_warnings: list[ValidationMessage],
) -> tuple[dict[str, Any], int]:
    final_layout, errors, warnings, repaired = validate_or_repair_layout(layout_json, image_name)
    all_warnings = extra_warnings + warnings
    status = "SUCCESS" if not errors else "FAILED"
    preview_html = ""
    if status == "SUCCESS":
        preview_html, compiler_warnings, _ = compile_preview_html(final_layout)
        all_warnings += compiler_warnings
    # ...
```

**问题 3：`ai_warnings` 变量作用域混乱**

```python
ai_warnings: list[ValidationMessage] = []   # 第 462 行
try:
    ...
    all_warnings = ai_warnings + warnings   # 第 467 行
    ...
    ai_warnings = all_warnings + [...]       # 第 487 行 — 覆盖了上面的引用
except RealAIError:
    ai_warnings.append(...)                  # 第 491 行
```

变量在 try 块前初始化、在 try 块内被覆盖、在 except 块里被 append，逻辑难以追踪。

---

### 3.4 `real_ai_layout_client.py` — 最干净，评分 8/10

**优点：**
- 异常层次清晰：`RealAIError` → `RealAIUnavailableError` / `RealAIResponseError`
- `parse_json_payload()` markdown code fence 回退提取实用
- `extract_chat_completion_text()` 处理 string/list 两种格式

**待改进：**
- `detect_image_mime_type()` 可用标准库 `mimetypes.guess_type()` 替代
- 缺少超时配置（当前阶段可接受，接入真实 AI 后需补充）

---

### 3.5 `image_layout_resolver.py` — 简洁但启发式弱，评分 7/10

**待改进：**
- `infer_template_key_from_image_name()` 用文件名关键词匹配太宽泛，`"card"` 一词匹配范围过大
- `TEMPLATE_FIXTURES` 里包含 `invalid-layout`（测试用 fixture），不应出现在生产模板注册表

建议将 `invalid-layout` 从生产注册表移除，仅在测试中使用：

```python
TEMPLATE_FIXTURES = {
    "landing-basic": "landing-basic.layout.json",
    "card-list": "card-list.layout.json",
}
```

---

### 3.6 `main.py` — 清晰，评分 8/10

无大问题。`str_to_bool()` 实用，参数校验清晰。`try/except ImportError` 双路径在加 `__init__.py` 后可删除。

---

## 四、安全方面评价

安全意识是本模块最大亮点，评分 9/10：

- CSS 值白名单校验（颜色、长度、flex 值等）
- `FORBIDDEN_HTML_SNIPPETS` 黑名单拦截 `<script>`、`onclick=`、`javascript:`
- `is_safe_image_src()` 阻止 `javascript:`、`data:`、路径穿越
- `html.escape()` 对所有用户文本做 XSS 转义
- `enforce_preview_html_safety()` 最终输出的二次防御

---

## 五、整体评分

| 维度 | 评分 | 说明 |
|------|------|------|
| 模块职责划分 | 8/10 | validator / generator / resolver / client 各司其职 |
| 函数粒度 | 7/10 | `process_image_layout_job` 和 `compile_node` 偏大 |
| 安全意识 | 9/10 | XSS、CSS 注入、图片 src 校验到位 |
| 测试覆盖 | 8/10 | 5 个测试文件覆盖主要路径和边界 |
| DRY（不重复） | 5/10 | 跨模块重复较多，pipeline 内部也重复 |
| 工程规范 | 4/10 | 缺 `__init__.py`、`pyproject.toml`、测试目录分离 |
| 类型标注 | 8/10 | 全部函数有类型标注，用了 `str \| Path` 新语法 |
| 错误处理 | 7/10 | 异常层次清晰，但 pipeline 里 `except Exception` 太宽 |

---

## 六、优先级排序

### P0 — 尽快修复

1. **加 `__init__.py`**，删除所有 `try: from . import ... except ImportError` 双路径 import
2. **加 `pyproject.toml`**，声明 `openai` 依赖和 pytest 配置
3. **拆 `tests/` 目录**，测试文件从 worker 根目录移入 `tests/`

### P1 — 下一个迭代

4. **提取 `common.py`**，消除 `message_to_dict` / `make_message` / `configure_output_encoding` 重复
5. **重构 `process_image_layout_job()`**，抽取 `_finalize_layout()` 消除重复流程
6. **用 dataclass 替代 10 参数 `make_result()`**

### P2 — 后续优化

7. `safe_css_value()` 用字典映射替代 if-elif 链
8. `TEMPLATE_FIXTURES` 移除 `invalid-layout`
9. 统一错误信息语言风格（全英文或全中文）
10. `detect_image_mime_type()` 用 `mimetypes` 标准库替代
