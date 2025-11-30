# 📚 课程目录 (Table of Contents)

* [概述](#概述)
    * [课程说明](#课程说明)
    * [学分](#学分)
    * [先决条件](#先决条件)
    * [形式](#形式)
    * [目标](#目标)
    * [答疑时间](#答疑时间)
    * [团队](#团队)
* [教学大纲](#教学大纲)
    * [课程表](#课程表)
        * [第 1 周：LLM 编码和 AI 开发导论](#第-1-周llm-编码和-ai-开发导论)
        * [第 2 周：编码 Agent 的剖析](#第-2-周编码-agent-的剖析)
        * [第 3 周：AI IDE](#第-3-周ai-ide)
        * [第 4 周：编码 Agent 模式](#第-4-周编码-agent-模式)
        * [第 5 周：现代 Terminal](#第-5-周现代-terminal)
        * [第 6 周：AI 测试与安全](#第-6-周ai-测试与安全)
        * [第 7 周：现代软件支持](#第-7-周现代软件支持)
        * [第 8 周：自动化 UI 和应用构建](#第-8-周自动化-ui-和应用构建)
        * [第 9 周：Agent 部署后](#第-9-周agent-部署后)
        * [第 10 周：AI 软件工程的未来](#第-10-周ai-软件工程的未来)
    * [评分](#评分)
* [FAQ](#faq)
    * [常见问题](#常见问题)
    * [联系信息](#联系信息)


# 概述

## 课程说明

在过去的几年里，**大型语言模型**（**LLM**）在软件开发领域引入了一种革命性的新范式。传统的软件开发生命周期正在被每个阶段的 **AI** 自动化所改变，这引出了一个问题：下一代软件工程师应该如何利用这些进步来将其生产力提高 **10 倍**，并为他们的职业生涯做准备？

本课程将证明，现代 **AI** 工具不仅能提高开发人员的生产力，还能使软件工程对更广泛的受众实现**民主化**。我们将展示，软件开发已从 **0-1** 代码创建演变为一个“计划、用 **AI** 生成、修改和重复”的迭代工作流程。学生将掌握传统软件工程挑战背后的理论，以及现今解决这些挑战的**尖端 AI 驱动工具**。

通过**动手工程任务**以及来自构建这些革命性工具的**行业先驱**的演讲，您将获得 **AI** 辅助开发、**自动化测试**、**智能文档**和**安全漏洞检测**的实践经验。到本课程结束时，您将对如何将**最先进的 LLM 模型**整合到复杂的开发工作流程中并避免常见陷阱有一个清晰的理解。

### 学分

3 学分

### 先决条件

**CS111** 同等编程经验。推荐 **CS221/229**。

### 形式

每周讲座、动手编码会话和行业客座讲师。展示现代开发实践的期末项目。

### 目标

掌握现代开发工具，理解 **AI** 辅助编码，学习自动化测试和部署，探索新兴的软件趋势。

### 教室

420-041

### 答疑时间

**Mihail Eric：** 周五 12:00-12:30 PM

**Febie Lin：** 周三 9:00-11:00 AM (Huang 地下室)

### 作业截止日期

[日历](https://docs.google.com/spreadsheets/d/1-485SLHw_zn7A-UXiz88Dgjy_qUGx87Am6HUwQrKsN8/edit?gid=0#gid=0)

---

## 团队

---

# 教学大纲

## 课程表

### 第 1 周：LLM 编码和 AI 开发导论

**主题**

- 课程安排
    
- **LLM** 到底是什么
    
- 如何有效进行 **prompt**
    

**阅读材料**

- [Deep Dive into LLMs](https://www.youtube.com/watch?v=7xTGNNLPyMI)
    
- [Prompt Engineering Overview](https://cloud.google.com/discover/what-is-prompt-engineering)
    
- [Prompt Engineering Guide](https://www.promptingguide.ai/techniques)
    
- [AI Prompt Engineering: A Deep Dive](https://www.youtube.com/watch?v=T9aRN5JkmL8)
    
- [How OpenAI Uses Codex](https://cdn.openai.com/pdf/6a2631dc-783e-479b-b1a4-af0cfbd38630/how-openai-uses-codex.pdf)
    

**作业**

- [LLM Prompting Playground](https://github.com/mihail911/modern-software-dev-assignments/tree/master/week1)
    

**9月22日周一：** 导论和 **LLM** 的制作方式 - [Slides](https://docs.google.com/presentation/d/1zT2Ofy88cajLTLkd7TcuSM4BCELvF9qQdHmlz33i4t0/edit?usp=sharing)

**9月26日周五：** 强大的 **LLM prompt** - [Slides](https://docs.google.com/presentation/d/1MIhw8p6TLGdbQ9TcxhXSs5BaPf5d_h77QY70RHNfeGs/edit?usp=drive_link)

---

### 第 2 周：编码 Agent 的剖析

**主题**

- **Agent** 架构和组件
    
- 工具使用和函数调用
    
- **MCP (Model Context Protocol)**
    

**阅读材料**

- [MCP Introduction](https://stytch.com/blog/model-context-protocol-introduction/)
    
- [Sample MCP Server Implementations](https://github.com/modelcontextprotocol/servers)
    
- [MCP Server Authentication](https://developers.cloudflare.com/agents/guides/remote-mcp-server/#add-authentication)
    
- [MCP Server SDK](https://github.com/modelcontextprotocol/typescript-sdk/tree/main?tab=readme-ov-file#server)
    
- [MCP Registry](https://blog.modelcontextprotocol.io/posts/2025-09-08-mcp-registry-preview/)
    
- [MCP Food-for-Thought](https://www.reillywood.com/blog/apis-dont-make-good-mcp-tools/)
    

**作业**

- [First Steps in the AI IDE](https://github.com/mihail911/modern-software-dev-assignments/tree/master/week2)
    

**9月29日周一：** 从头构建一个编码 **Agent** - [Slides](https://docs.google.com/presentation/d/11CP26VhsjnZOmi9YFgLlonzdib9BLyAlgc4cEvC5Fps/edit?usp=sharing)，[Completed Exercise](https://drive.google.com/file/d/1YtpKFVG13DHyQ2i3HOtwyVJOV90nWeL2/view?usp=drive_link)

**10月3日周五：** 构建一个自定义 **MCP** 服务器- [Slides](https://docs.google.com/presentation/d/1zSC2ra77XOUrJeyS85houg1DU7z9hq5Y4ebagTch-5o/edit?usp=drive_link)，[Completed Exercise](https://drive.google.com/file/d/1J6lgZWcxPzpCpjujJSnW1aAkCYF6Yxv3/view?usp=drive_link)

---

### 第 3 周：AI IDE

**主题**

- 上下文管理和代码理解
    
- **Agent** 的 **PRD**
    
- **IDE** 集成和扩展
    

**阅读材料**

- [Specs Are the New Source Code](https://blog.ravi-mehta.com/p/specs-are-the-new-source-code)
    
- [How Long Contexts Fail](https://www.dbreunig.com/2025/06/22/how-contexts-fail-and-how-to-fix-them.html)
    
- [Devin: Coding Agents 101](https://devin.ai/agents101#introduction)
    
- [Getting AI to Work In Complex Codebases](https://github.com/humanlayer/advanced-context-engineering-for-coding-agents/blob/main/ace-fca.md)
    
- [How FAANG Vibe Codes](https://x.com/rohanpaul_ai/status/1959414096589422619)
    
- [Writing Effective Tools for Agents](https://www.anthropic.com/engineering/writing-tools-for-agents)
    

**作业**

- [Build a Custom MCP Server](https://github.com/mihail911/modern-software-dev-assignments/blob/master/week3/assignment.md)
    

**10月6日周一：** 从第一个 **prompt** 到最佳 **IDE** 设置 - [Slides](https://docs.google.com/presentation/d/11pQNCde_mmRnImBat0Zymnp8TCS_cT_1up7zbcj6Sjg/edit?usp=sharing)，[Design Doc Template](https://drive.google.com/file/d/1MZ0Qx68Vzw4x5x_XcV8XiPLp7fFDe1LJ/view?usp=drive_link)

**10月10日周五：** Cognition [研究负责人](https://cognition.ai/) Silas Alberti - [Slides](https://docs.google.com/presentation/d/1i0pRttHf72lgz8C-n7DSegcLBgncYZe_ppU7dB9zhUA/edit?usp=sharing)

---

### 第 4 周：编码 Agent 模式

**主题**

- 管理 **Agent** 自治级别
    
- 人机 **Agent** 协作模式
    

**阅读材料**

- [How Anthropic Uses Claude Code](https://www-cdn.anthropic.com/58284b19e702b49db9302d5b6f135ad8871e7658.pdf)
    
- [Claude Best Practices](https://www.anthropic.com/engineering/claude-code-best-practices)
    
- [Awesome Claude Agents](https://github.com/vijaythecoder/awesome-claude-agents)
    
- [Super Claude](https://github.com/SuperClaude-Org/SuperClaude_Framework)
    
- [Good Context Good Code](https://blog.stockapp.com/good-context-good-code/)
    
- [Peeking Under the Hood of Claude Code](https://medium.com/@outsightai/peeking-under-the-hood-of-claude-code-70f5a94a9a62)
    

**作业**

- [Coding with Claude Code](https://github.com/mihail911/modern-software-dev-assignments/blob/master/week4/assignment.md)
    

**10月13日周一：** 如何成为一名 **Agent** 管理者 - [Slides](https://docs.google.com/presentation/d/19mgkwAnJDc7JuJy0zhhoY0ZC15DiNpxL8kchPDnRkRQ/edit?usp=sharing)

**10月17日周五：** [Claude Code](https://www.anthropic.com/claude-code) 创作者 Boris Cherney - [Slides](https://docs.google.com/presentation/d/1bv7Zozn6z45CAh-IyX99dMPMyXCHC7zj95UfwErBYQ8/edit?usp=sharing)

---

### 第 5 周：现代 Terminal

**主题**

- **AI** 增强的命令行界面
    
- **Terminal** 自动化和脚本编写
    

**阅读材料**

- [Warp University](https://www.warp.dev/university?slug=university)
    
- [Warp vs Claude Code](https://www.warp.dev/university/getting-started/warp-vs-claude-code)
    
- [How Warp Uses Warp to Build Warp](https://notion.warp.dev/How-Warp-uses-Warp-to-build-Warp-21643263616d81a6b9e3e63fd8a7380c)
    

**作业**

- [Agentic Development with Warp](https://github.com/mihail911/modern-software-dev-assignments/tree/master/week5)
    

**10月20日周一：** 如何打造一款突破性的 **AI** 开发者产品 - [Slides](https://docs.google.com/presentation/d/1Djd4eBLBbRkma8rFnJAWMT0ptct_UGB8hipmoqFVkxQ/edit?usp=sharing)

**10月24日周五：** [Warp](https://www.warp.dev/) **CEO** Zach Lloyd - [Slides](https://www.figma.com/slides/kwbcmtqTFQMfUhiMH8BiEx/Warp---Stanford--Copy-?node-id=9-116&t=oBWBCk8mjg2l2NR5-1)

---

### 第 6 周：AI 测试与安全

**主题**

- 安全的 **vibe** 编码
    
- 漏洞检测的历史
    
- **AI** 生成的测试套件
    

**阅读材料**

- [SAST vs DAST](https://www.splunk.com/en_us/blog/learn/sast-vs-dast.html)
    
- [Copilot Remote Code Execution via Prompt Injection](https://embracethered.com/blog/posts/2025/github-copilot-remote-code-execution-via-prompt-injection/)
    
- [Finding Vulnerabilities in Modern Web Apps Using Claude Code and OpenAI Codex](https://semgrep.dev/blog/2025/finding-vulnerabilities-in-modern-web-apps-using-claude-code-and-openai-codex/)
    
- [Agentic AI Threats: Identity Spoofing and Impersonation Risks](https://www.google.com/search?q=https://unit42.paloaltonetworks.com/agentic-ai-threats/%23:~:text%3DIdentity%2520spoofing%2520and%2520impersonation:%2520Attackers,accurate%2520information%2520exchange%2520are%2520critical.)
    
- [OWASP Top Ten: The Leading Web Application Security Risks](https://owasp.org/www-project-top-ten/)
    
- [Context Rot: Understanding Degradation in AI Context Windows](https://research.trychroma.com/context-rot)
    
- [Vulnerability Prompt Analysis with O3](https://github.com/SeanHeelan/o3_finds_cve-2025-37899/blob/master/system_prompt_uafs.prompt)
    

**作业**

- [Writing Secure AI Code](https://github.com/mihail911/modern-software-dev-assignments/blob/master/week6/assignment.md)
    

**10月27日周一：** **AI QA**、**SAST**、**DAST** 及其他 - [Slides](https://docs.google.com/presentation/d/1C05bCLasMDigBbkwdWbiz4WrXibzi6ua4hQQbTod_8c/edit?usp=sharing)

**10月31日周五：** [Semgrep](https://semgrep.dev/) **CEO** Isaac Evans

---

### 第 7 周：现代软件支持

**主题**

- 我们可以信任哪些 **AI** 代码系统
    
- 调试和诊断
    
- 智能文档生成
    

**阅读材料**

- [Code Reviews: Just Do It](https://blog.codinghorror.com/code-reviews-just-do-it/)
    
- [How to Review Code Effectively](https://github.blog/developer-skills/github/how-to-review-code-effectively-a-github-staff-engineers-philosophy/)
    
- [AI-Assisted Assessment of Coding Practices in Modern Code Review](https://arxiv.org/pdf/2405.13565)
    
- [AI Code Review Implementation Best Practices](https://graphite.dev/guides/ai-code-review-implementation-best-practices)
    
- [Code Review Essentials for Software Teams](https://blakesmith.me/2015/02/09/code-review-essentials-for-software-teams.html)
    
- [Lessons from millions of AI code reviews](https://www.youtube.com/watch?v=TswQeKftnaw)
    

**作业**

- [Code Review Reps](https://github.com/mihail911/modern-software-dev-assignments/tree/master/week7)
    

**11月3日周一：** **AI** 代码审查 - [Slides](https://docs.google.com/presentation/d/1NkPzpuSQt6Esbnr2-EnxM9007TL6ebSPFwITyVY-QxU/edit?usp=sharing)

**11月7日周五：** [Graphite](https://graphite.dev/) **CPO** Tomas Reimers - [Slides](https://drive.google.com/file/d/1hwF-RIkOJ_OFy17BKhzFyCtxSS7Pcf7p/view?usp=drive_link)

---

### 第 8 周：自动化 UI 和应用构建

**主题**

- 每个人都能进行设计和前端
    
- 快速 **UI/UX** 原型设计和迭代
    

**作业**

- [Multi-stack Web App Builds](https://github.com/mihail911/modern-software-dev-assignments/tree/master/week8)
    

**11月10日周一：** 单个 **prompt** 实现端到端应用 - [Slides](https://docs.google.com/presentation/d/1GrVLsfMFIXMiGjIW9D7EJIyLYh_-3ReHHNd_vRfZUoo/edit?usp=sharing)

**11月14日周五：** [Vercel](https://vercel.com/) **AI** 研究负责人 Gaspar Garcia - [Slides](https://docs.google.com/presentation/d/1Jf2aN5zIChd5tT86rZWWqY-iDWbxgR-uynKJxBR7E9E/edit?usp=sharing)

---

### 第 9 周：Agent 部署后

**主题**

- **AI** 系统的监控和可观测性
    
- 自动化事件响应
    
- 分诊和调试
    

**11月17日周一：** 事件响应和 **DevOps** - [Slides](https://docs.google.com/presentation/d/1Mfe-auWAsg9URCujneKnHr0AbO8O-_U4QXBVOlO4qp0/edit?usp=sharing)

**11月21日周五：** [Resolve](https://resolve.ai/) **CTO** Mayank Agarwal 和 [Resolve](https://resolve.ai/) 技术人员 Milind Ganjoo - [Slides](https://drive.google.com/file/d/11WnEbMGc9kny_WBpMN10I8oP8XsiQOnM/view?usp=sharing)

---

### 第 10 周：AI 软件工程的未来

**主题**

- 软件开发角色的未来
    
- 新兴的 **AI** 编码范式
    
- 行业趋势和预测
    

**12月1日周一：** 10 年后的软件开发

**12月5日周五：** [a16z](https://a16z.com/) 普通合伙人

---

## 评分

期末项目 80%

每周作业 15%

课堂参与 5%

---

# FAQ

## 常见问题

#### 本课程将使用哪些编程语言？

本课程与语言无关，重点关注适用于不同编程语言的工具和实践。但是，示例将主要使用 **Python**、**JavaScript** 和一些系统编程语言（在适当的情况下）。重点是理解现代开发实践，而不是掌握特定语言。

#### 我是否需要有使用 GitHub Copilot 等 AI 工具的经验？

不需要有使用 **AI** 开发工具的先验经验。本课程将从基础开始，逐步过渡到更高级的用法。但是，扎实的编程基础（**CS111** 及以上）是必不可少的。

#### 本课程会取代传统的软件工程课程吗？

本课程通过关注现代工具和 **AI** 辅助开发来补充传统的软件工程课程。它假定您拥有基础的软件工程知识，并在此基础上构建当代实践。

#### 本课程的时间投入是多少？

预计每周大约需要 **10-12** 小时，包括讲座、作业和项目工作。本课程的动手性质要求有时间进行新工具和技术的实验。

#### 有任何特殊的软件或硬件要求吗？

学生需要一台能够运行现代开发工具的计算机。一些基于云的服务可能需要订阅（**GitHub Copilot** 等），但课程将在可能的情况下提供访问权限或替代方案。可靠的互联网连接对于基于云的工具至关重要。

#### 课程内容将有多新？

课程内容的设计旨在保持高度的**时效性**，每周都会更新以反映 **AI** 辅助开发领域快速发展的现状。来自**领先公司**的客座讲师确保学生了解最新的行业实践和新兴工具。

#### 我可以旁听本课程吗？

我们对斯坦福大学的学生和教职员工的旁听请求持开放态度。您将能够参加所有讲座，但我们无法对您的作业评分或提供期末项目建议。

---

## 联系信息

**课程邮箱：** 待定 (**TBA**)

**Ed Discussion：** 将向注册学生提供链接

**Canvas：** 所有课程材料和提交均通过 Stanford Canvas 进行
