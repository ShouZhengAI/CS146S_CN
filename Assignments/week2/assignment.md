# 第 2 周——行动项提取器

本周，我们将在一个精简的 FastAPI + SQLite 应用基础上进行扩展。该应用能够将自由格式的笔记转换为按条目列出的行动项。

***建议在开始之前完整阅读本文档。***

提示：如需预览此 Markdown 文件
- 在 Mac 上，按 `Command (⌘) + Shift + V`
- 在 Windows/Linux 上，按 `Ctrl + Shift + V`


## 开始使用

### 配置 Cursor
请按照以下说明配置 Cursor 并打开你的项目：
1. 领取一年免费 Cursor Pro：https://cursor.com/students
2. 下载 Cursor：https://cursor.com/download
3. 如需启用 Cursor 命令行工具，请打开 Cursor。Mac 用户按 `Command (⌘) + Shift + P`（非 Mac 用户按 `Ctrl + Shift + P`）打开命令面板。输入：`Shell Command: Install 'cursor' command`。选中该命令并按 Enter 键。
4. 打开一个新的终端窗口，进入项目根目录，然后运行：`cursor .`

### 当前应用
你可以按照以下步骤运行当前的初始应用：
1. 激活你的 conda 环境。
```
conda activate cs146s 
```
2. 在项目根目录下运行服务器：
```
poetry run uvicorn week2.app.main:app --reload
```
3. 打开 Web 浏览器并访问 http://127.0.0.1:8000/。
4. 熟悉应用当前的状态。请确保你能够成功输入笔记，并生成提取后的行动项核对清单。

## 练习
在每项练习中，使用 Cursor 协助你为当前的行动项提取器应用实现指定的改进。

完成作业的过程中，请使用 `writeup.md` 记录你的进展。务必包含你使用的提示词，以及你本人或 Cursor 所做的任何更改。我们将根据作业报告的内容进行评分。另请在代码中添加注释，记录你所做的更改。

### TODO 1：搭建新功能的基本框架

分析 `week2/app/services/extract.py` 中现有的 `extract_action_items()` 函数；该函数目前使用预定义的启发式规则提取行动项。

你的任务是实现一个由**大语言模型（LLM）驱动**的替代函数 `extract_action_items_llm()`，该函数使用 Ollama，通过大语言模型完成行动项提取。

一些提示：
- 如需生成结构化输出（即字符串组成的 JSON 数组），请参阅此文档：https://ollama.com/blog/structured-outputs
- 如需浏览可用的 Ollama 模型，请参阅此页面：https://ollama.com/library。请注意，模型越大，消耗的计算资源越多，因此建议从较小的模型开始。如需拉取并运行模型，请执行：`ollama run {MODEL_NAME}`

### TODO 2：添加单元测试

在 `week2/tests/test_extract.py` 中为 `extract_action_items_llm()` 编写单元测试，覆盖多种输入（例如项目符号列表、带关键字前缀的行以及空输入）。

### TODO 3：重构现有代码以提升清晰度

重构后端代码，重点关注定义明确的 API 契约/模式、数据库层清理、应用生命周期/配置以及错误处理。

### TODO 4：使用智能体模式自动完成小型任务

1. 将由 LLM 驱动的提取功能集成为一个新端点。更新前端，添加“使用 LLM 提取”按钮；点击后，该按钮应通过新端点触发提取流程。

2. 提供最后一个用于检索所有笔记的端点。更新前端，添加“列出笔记”按钮；点击后，该按钮应获取并显示所有笔记。

### TODO 5：根据代码库生成 README

***学习目标：***
*学生将学习 AI 如何分析代码库并自动生成文档，从而展示 Cursor 解析代码上下文并将其转化为人类可读内容的能力。*

使用 Cursor 分析当前代码库并生成一份结构清晰的 `README.md` 文件。README 至少应包含：
- 项目简介
- 项目的配置与运行方法
- API 端点及其功能
- 运行测试套件的说明

## 提交内容
请按照提供的说明填写 `week2/writeup.md`。确保你所做的所有更改均已记录在代码库中。

## 评分标准（总计 100 分）
- 第 1～5 部分每部分 20 分（生成的代码占 10 分，每部分使用的提示词占 10 分）。
