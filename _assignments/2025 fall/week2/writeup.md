# 第 2 周作业报告

## 提交信息

姓名：**未提供**  
SUNet ID：**未提供**  
引用来源：**Ollama Structured Outputs 文档（https://ollama.com/blog/structured-outputs）、FastAPI 文档（https://fastapi.tiangolo.com/）**

我大约花了 **3** 小时完成本次作业。

## 你的回答

### 练习 1：搭建新功能的基本框架

提示词：

```text
分析现有 extract_action_items，并实现 extract_action_items_llm(text)。使用 Ollama chat 和 JSON Schema 结构化输出；兼容对象/字典响应、JSON 代码块、空项和重复项。空输入不要调用模型，模型不可用或返回非法 JSON 时回退到本地规则。模型名允许用环境变量配置。
```

生成的代码位置：

```text
week2/app/services/extract.py:20-30
  定义 action_items 结构化输出 JSON Schema。
week2/app/services/extract.py:81-120
  读取 Ollama 响应并稳健解析、清理、去重。
week2/app/services/extract.py:123-150
  调用 Ollama chat；处理空输入并在任何模型/解析异常时回退。
```

主要改动：新增 `ACTION_ITEMS_SCHEMA`、`_response_content()`、`_parse_action_items()` 和 `extract_action_items_llm()`；保留原规则函数作为离线兜底。

反思：只依赖模型“按提示返回 JSON”不够稳定。Schema 负责约束正常路径，解析兼容和规则回退负责异常路径，这样本机模型未启动时应用仍可使用。

### 练习 2：添加单元测试

提示词：

```text
为 extract_action_items_llm 编写不访问网络的单元测试。mock Ollama chat，覆盖项目符号、TODO/Action/Next 前缀、空输入、普通无任务文本、结构化响应、非法响应回退、重复项和 JSON 代码块；同时验证传给 Ollama 的 format 与 temperature。
```

生成的代码位置：

```text
week2/tests/test_extract.py:22-75
  新增 6 个 LLM 测试，覆盖规则回退、空输入、无结构文本、mock
  结构化响应、大小写去重和 Markdown JSON 代码块。
```

主要改动：使用 `unittest.mock.patch` 替换 `chat`，并用字典与 `SimpleNamespace` 两种对象模拟 Ollama 的可能返回形式。

反思：真实模型输出有随机性且依赖本机服务，不适合作为单元测试依赖。mock 能稳定验证调用契约和解析行为，异常返回测试则确保回退不是只写未测。

### 练习 3：重构现有代码以提升清晰度

提示词：

```text
在不改变原规则提取行为的前提下整理代码：把 Ollama 响应读取、JSON 解析和模型调用分开；清除 main.py 未使用导入；路由统一做空文本检查，并让数据库读写继续集中在 db.py。避免新增无必要抽象。
```

生成/修改的代码位置：

```text
week2/app/services/extract.py:81-120
  将响应适配和数据规范化拆成可单独理解的小函数。
week2/app/main.py:2-20
  删除未使用导入，并用 FastAPI lifespan 在应用启动时初始化数据库。
week2/app/routers/notes.py:28-50
  返回字段固定的笔记列表和 LLM 提取响应，并复用 db.py 持久化函数。
week2/frontend/index.html:39-144
  抽出 requestJson、renderMessage、renderItems 和 extract，统一错误显示。
```

主要改动：模型相关职责分层，API 返回保持 `{note_id, items}` 结构，前端请求与渲染逻辑复用；没有把 SQL 或模型细节泄漏到页面代码。

反思：重构的重点不是增加类，而是分离变化原因。模型响应格式、行动项清洗和 HTTP 交互会独立变化，拆开后更容易测试和维护。

### 练习 4：使用智能体模式自动完成小型任务

提示词：

```text
新增 GET /notes，按数据库顺序返回全部笔记；新增 POST /notes/extract-llm，接收 text 和 save_note，调用 LLM 提取并保存关联行动项。网页增加“使用 LLM 提取”和“列出笔记”按钮，显示加载、空结果和错误状态。用户文本必须通过 DOM textContent 渲染，不能拼接 innerHTML。
```

生成的代码位置：

```text
week2/app/routers/notes.py:28-34
  GET /notes 列出全部笔记。
week2/app/routers/notes.py:37-50
  POST /notes/extract-llm 调用模型、可选保存笔记并保存行动项。
week2/frontend/index.html:11-19
  新增按钮状态、笔记卡片和错误样式。
week2/frontend/index.html:28-36
  新增两个按钮及独立结果容器。
week2/frontend/index.html:39-144
  新增 API 调用、行动项渲染、LLM 提取和笔记列表逻辑。
```

主要改动：补齐两个接口和端到端页面交互；显示内容使用 `textContent`，避免笔记或模型文本被当成 HTML 执行。

反思：一个按钮功能不仅是发请求，还要覆盖等待、成功、空数组和失败四种状态。分开行动项与笔记容器后，两类结果不会互相覆盖。

### 练习 5：根据代码库生成 README

提示词：

```text
阅读 week2 的应用入口、数据库、路由、提取服务、前端和测试，生成中文 README。包含项目简介、Poetry/Ollama 配置、启动步骤、环境变量、完整 API 表、响应示例、测试命令、目录结构，以及练习 1-5 的简短、通俗、准确解题思路。
```

生成的代码位置：

```text
week2/README.md:1-123
  新增完整项目文档，包括介绍、环境配置、启动、API、测试、目录结构
  和五项练习的解题思路。
```

主要改动：从空缺状态新增 README，记录默认模型 `llama3.2:3b`、`OLLAMA_MODEL` 配置、所有接口及 mock 测试说明。

反思：README 应以新用户能否照着跑起来为标准。命令、端口、模型名、请求体和失败回退都明确写出，比只描述代码结构更实用。
