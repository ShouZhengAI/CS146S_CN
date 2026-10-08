# 第 4 周——现实世界中的自主编码智能体

> ***建议在开始之前完整阅读本文档。***

本周，你的任务是在本仓库的环境中，使用以下任意组合的 **Claude Code** 功能构建至少 **2 个自动化工作流**：


- 自定义斜杠命令（提交至 `.claude/commands/*.md`）

- 用于提供仓库或上下文指导的 `CLAUDE.md` 文件

- Claude 子智能体（协同工作的角色专用智能体）

- 集成到 Claude Code 中的 MCP 服务器

你的自动化工作流应当切实改进开发者工作流程，例如简化测试、文档编写、重构或数据相关任务。随后，你将使用自己创建的自动化工作流，进一步扩展 `week4/` 中的初始应用程序。


## 了解 Claude Code
为了更深入地理解 Claude Code 并探索可选的自动化方案，请阅读以下两份资料：

1. **Claude Code 最佳实践：** [anthropic.com/engineering/claude-code-best-practices](https://www.anthropic.com/engineering/claude-code-best-practices)

2. **子智能体概述：** [docs.anthropic.com/en/docs/claude-code/sub-agents](https://docs.anthropic.com/en/docs/claude-code/sub-agents)

## 探索初始应用程序
这是一个最小化的全栈初始应用程序，旨在成为一个**“开发者指挥中心”**。
- 使用 SQLite（SQLAlchemy）的 FastAPI 后端
- 静态前端（无需 Node 工具链）
- 最小化测试集（pytest）
- Pre-commit（black + ruff）
- 用于练习智能体驱动工作流的任务

请将此应用程序作为试验场，尝试你所构建的 Claude 自动化工作流。

### 目录结构

```
backend/                # FastAPI 应用程序
frontend/               # 由 FastAPI 提供服务的静态界面
data/                   # SQLite 数据库与种子数据
docs/                   # 用于智能体驱动工作流的任务清单
```

### 快速开始

1) 激活你的 conda 环境。

```bash
conda activate cs146s
```

2) （可选）安装 pre-commit 钩子

```bash
pre-commit install
```

3) 运行应用程序（在 `week4/` 目录中执行）

```bash
make run
```

4) 打开 `http://localhost:8000` 查看前端，打开 `http://localhost:8000/docs` 查看 API 文档。

5) 尝试使用初始应用程序，以了解其当前的特性和功能。


### 测试
运行测试（在 `week4/` 目录中执行）
```bash
make test
```

### 格式化/代码检查
```bash
make format
make lint
```

## 第一部分：构建你的自动化工作流（选择 2 项或更多）
现在你已经熟悉了初始应用程序，下一步是构建自动化工作流来增强或扩展它。下面列出了几类可供选择的自动化方案，你可以跨类别自由组合。

构建自动化工作流时，请在 `writeup.md` 文件中记录你的改动。暂时将*“你如何使用自动化工作流增强初始应用程序”*一节留空——你将在作业的第二部分回到这里继续填写。

### A) Claude 自定义斜杠命令
斜杠命令是一项面向重复性工作流程的功能，你可以在 `.claude/commands/` 内的 Markdown 文件中创建可复用的工作流程。Claude 会通过 `/` 提供这些命令。


- 示例 1：带覆盖率统计的测试运行器
  - 名称：`tests.md`
  - 目的：运行 `pytest -q backend/tests --maxfail=1 -x`，若测试通过，再运行覆盖率统计。
  - 输入：可选的标记或路径。
  - 输出：汇总失败情况并建议后续步骤。
- 示例 2：文档同步
  - 名称：`docs-sync.md`
  - 目的：读取 `/openapi.json`，更新 `docs/API.md`，并列出路由差异。
  - 输出：类似 diff 的摘要和待办事项。
- 示例 3：重构工具
  - 名称：`refactor-module.md`
  - 目的：重命名模块（例如 `services/extract.py` → `services/parser.py`）、更新导入，并运行代码检查和测试。
  - 输出：修改文件清单和验证步骤。

>*提示：确保命令职责明确，使用 `$ARGUMENTS`，并优先采用幂等步骤。可考虑将安全工具加入允许列表，并使用无头模式来保证可重复性。*

### B) `CLAUDE.md` 指导文件
开始对话时会自动读取 `CLAUDE.md` 文件，因此你可以用它提供会影响 Claude 行为的仓库专用指令、上下文或指导。请在仓库根目录中创建一个 `CLAUDE.md`（也可选择在 `week4/` 的子文件夹中创建），以指导 Claude 的行为。

- 示例 1：代码导航和入口点
  - 包含内容：如何运行应用程序、路由器所在位置（`backend/app/routers`）、测试所在位置，以及数据库如何填充种子数据。
- 示例 2：代码风格与安全防护规则
  - 包含内容：工具使用要求（black/ruff）、可以安全运行的命令、应避免的命令，以及代码检查/测试门禁。
- 示例 3：工作流程片段
  - 包含内容：“当被要求添加端点时，先编写一个失败的测试，然后实现功能，最后运行 pre-commit。”

> *提示：像迭代提示词一样持续改进 `CLAUDE.md`；内容应简洁且可执行，并记录你希望 Claude 使用的自定义工具/脚本。*

### C) 子智能体（角色专用）

子智能体是经过专门配置、用于处理特定任务的 AI 助手，拥有各自的系统提示词、工具和上下文。请设计两个或更多相互协作的智能体，每个智能体负责同一工作流程中的一个不同步骤。

- 示例 1：TestAgent + CodeAgent
  - 流程：TestAgent 为某项改动编写/更新测试 → CodeAgent 实现代码以通过测试 → TestAgent 进行验证。
- 示例 2：DocsAgent + CodeAgent
  - 流程：CodeAgent 添加新的 API 路由 → DocsAgent 更新 `API.md` 和 `TASKS.md`，并对照 `/openapi.json` 检查是否存在偏差。
- 示例 3：DBAgent + RefactorAgent
  - 流程：DBAgent 提出数据库模式变更（调整 `data/seed.sql`）→ RefactorAgent 更新模型、模式和路由器，并修复代码检查问题。

>*提示：使用清单/草稿区，在不同角色之间重置上下文（`/clear`），并让智能体并行执行相互独立的任务。*

## 第二部分：实际运用你的自动化工作流
现在你已经构建了 2 个或更多自动化工作流，让我们把它们投入使用！请在 `writeup.md` 的*“你如何使用自动化工作流增强初始应用程序”*一节中，说明你如何利用每个自动化工作流来改进或扩展应用程序的功能。

例如，如果你实现了自定义斜杠命令 `/generate-test-cases`，请说明你如何使用它与初始应用程序交互并对其进行测试。


## 提交内容
1) 两个或更多自动化工作流，可以包括：
   - `.claude/commands/*.md` 中的斜杠命令
   - `CLAUDE.md` 文件
   - 子智能体提示词/配置（需清楚记录；如有相关文件/脚本，也一并提交）

2) `week4/` 下的书面报告 `writeup.md`，其中应包括：
  - 设计灵感（例如引用最佳实践和/或子智能体文档）
  - 每个自动化工作流的设计，包括目标、输入/输出和步骤
  - 如何运行（准确命令）、预期输出，以及回滚/安全说明
  - 自动化前后对比（即手动工作流程与自动化工作流程的对比）
  - 你如何使用自动化工作流增强初始应用程序



## 提交说明
1. 确保已将所有更改推送到你的远程仓库，以供评分。
2. **确保已将 brentju 和 febielin 两人都添加为作业仓库的协作者。**
2. 通过 Gradescope 提交。


