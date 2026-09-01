<div align="center">
  <img src="Resource/imgs/teaser.png" width="100%" height="auto">
</div>

<h1 align="center">📚CS146S中文版课程 Vibe Coding Together</h1>

![Visitors](https://api.visitorbadge.io/api/visitors?path=https://github.com/ShouZhengAI/CS146S_CN&label=Total%20Visitors&labelColor=%232ccce4&countColor=%23d9e3f0)

> 本项目长期维护，希望能帮到各位入门 vibe coding 的朋友，欢迎Star，分享与提PR🌟~  
> 非官方项目、Fall 2025 已归档、Fall 2026 跟踪中、内容来源与版权归属原课程方。

🌟 付费赞助广告位：联系邮箱szwang.scholar@gmail.com，在文档内展示您的品牌和产品。

---
<table>
<tr>
<td width="180"><img src="Resource/imgs/ATLAS CLOUD LOGO_BLACK.png" alt="Atlas Cloud" width="150"></a></td>
<td><a href="https://www.atlascloud.ai/zh?utm_source=github&utm_medium=link&utm_campaign=CS146S_CN">Atlas Cloud</a> is a full-modal AI inference platform that gives developers a single AI API to access video generation, image generation, and LLM APIs. Instead of managing multiple vendor integrations, you connect once and get unified access to 300+ curated models across all modalities..

Check out Atlas Cloud's new coding plan promotion for more budget-friendly API access：<a href="https://www.atlascloud.ai/console/coding-plan">coding-plan</a>
</td>
</tr>
</tr>

<tr>
<td width="180"><img src="Resource/imgs/apimart.png" alt="Atlas Cloud" width="150"></a></td>
<td>
感谢 APIMart 赞助了本项目！APIMart 是专注 AI 图片/视频生成的低价 API 平台，GPT-Image-2 低至 $0.006/张，1 美元可出图 160+ 张。图片、视频一套异步 API 通吃，提交任务拿 ID、回调取结果，跑批万张不超时、换模型不改代码。按量付费、无月费，通过此<a href="https://go.apimart.ai/gh-cs146s_cn">注册链接</a>注册即可开用。

</td>
</tr>
</tr>

</table>




## 课程简介

大语言模型（LLM）正在把软件开发从以人工编写代码为主的过程，转变为开发者与能力日益增强的 Coding Agent 协作的过程。这一变化要求我们用新的方式定义意图、组织工作，并协调工具，让 Agent 能够有效参与复杂的软件项目。

课程将探讨 AI 原生软件开发背后的新兴实践与技术，包括 MCP、Agent Skills、spec-driven development、loop engineering 和 software factory。你将学习如何为 Agent 提供合适的上下文与能力，把产品需求转换为可执行的规格，并设计由人类与 Agent 共同规划、构建、评估和迭代改进的工作流。

通过动手作业、项目和来自下一代开发工具实践者的分享，学生将了解当前 Coding Agent 的能力与局限。课程结束时，学生将能够设计有效的 Agent 驱动工作流，将工具与 Skills 组合成可靠的开发系统，并运用 software factory 的原则，以更高的速度和规模构建、演进软件。


**先决条件**：具备相当于 CS111 级别的编程经验。推荐具备 CS221/229 课程知识。

**形式**：每周讲座、动手编码实践课，以及行业嘉宾演讲。期末项目要求展示现代开发实践。

**目标**：掌握现代开发工具、理解 AI 辅助编程、学习自动化测试和部署、探索新兴软件趋势。

**评分**：期末项目 50%，每周作业 15%，开源贡献 5%，课堂参与 5%

---
## 教学大纲
### Fall 2026（进行中，内容以官网发布为准）



| 周次     | 主题与要点                                                                                                                                                                                                                             | 课程安排                                                                                                                                                             |
| -------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 第 1 周  | **Coding Agent 的内部原理**<br>• LLM 究竟是什么，以及 Agent loop 在底层如何运行<br>• 核心工具集（read、write、edit、bash）及任务如何在其中流转<br>• 生产级 Coding Agent 如何组织 system prompt 与工具定义                              | **9/22（周二）**：课程简介 + 用 200 行代码构建 Claude Code<br>**9/24（周四）**：前沿 Coding Agent 的设计方式：深入剖析定义 Agent 的 system prompt                    |
| 第 2 周  | **高级 Context Engineering**<br>• 高级 prompting 技巧及其适用场景<br>• RePPIT（Research、Propose、Plan、Implement、Test）与 spec-driven development<br>• MCP 基础：server、client、tool 与 transport<br>• 为 Agent ergonomics 设计工具 | **9/29（周二）**：高级 prompting + Agentic 开发框架（RePPIT、spec-driven development）<br>**10/1（周四）**：MCP 与 tool calling 全面介绍（理论、配置与高级工具设计） |
| 第 3 周  | **Agent Skills 与 CLI**<br>• Skills 是什么；SKILL.md + 脚本如何编码一个工作流<br>• Web Skills，以及如何把 Agent 能力扩展到 repo 之外<br>• 如何高效地通过 CLI 工作                                                                      | **10/6（周二）**：全面了解 Agent Skills（含 Web Skills）<br>**10/8（周四）**：嘉宾：Lee Robinson（Cursor）                                                           |
| 第 4 周  | **定制你的 Agent 与仓库**<br>• CLAUDE.md 与 AGENTS.md：各自应该写什么<br>• 用 Hooks 配置 lint gate、测试运行与 guardrail<br>• Subagent 模式（planner / implementer / reviewer）                                                        | **10/13（周二）**：定制 Agentic 开发环境（CLAUDE.md、AGENTS.md、Hooks）<br>**10/15（周四）**：嘉宾：Boris Cherny（Anthropic），炉边问答                              |
| 第 5 周  | **Agent 就绪的代码库**<br>• 什么让 repo 对 Agent 友好：结构、文档、测试与检查机制<br>• 就绪度评分与审计<br>• 真实 repo 中阻碍 Agent 工作的常见缺口                                                                                     | **10/20（周二）**：让 repo 对 Agent 就绪：使仓库更 Agent-friendly 的结构、文档与检查机制<br>**10/22（周四）**：嘉宾：Eno Reyes，分享 Agent readiness                 |
| 第 6 周  | **Agentic Code Review**<br>• AI 代码审查擅长发现什么、又会遗漏什么<br>• 审查架构与自定义规则<br>• 将 AI 审查融入团队的 PR 工作流                                                                                                       | **10/27（周二）**：Agentic Code Review：最佳实践与架构<br>**10/29（周四）**：嘉宾：Silas Alberti（Cognition）                                                        |
| 第 7 周  | **安全**<br>• SAST / SCA、依赖漏洞与 Secret 泄露漏洞<br>• Prompt Injection 与 Agent 特有攻击面<br>• Agent 辅助的漏洞分诊与修复                                                                                                         | **11/3（周二）**：AI 代码库中的安全<br>**11/5（周四）**：嘉宾：Isaac Evans（Semgrep）                                                                                |
| 第 8 周  | **后台 Agent**<br>• 异步、云端委派的 Agent<br>• 管理并行 Agent 集群<br>• Issue-to-PR 流水线与触发器（Slack、Linear、GitHub）                                                                                                           | **11/10（周二）**：后台 Agent：异步启动任务<br>**11/12（周四）**：嘉宾（待公布）                                                                                     |
| 第 9 周  | **构建 AI 原生团队**<br>• MCP 门户与集中化、权限化的工具访问<br>• LLM gateway、模型路由与成本优化<br>• 组织范围内的落地模式                                                                                                            | **11/17（周二）**：大型团队中的 Coding Agent（MCP 门户、LLM gateway、组织模式、成本优化与模型路由）<br>**11/19（周四）**：嘉宾（待公布）                             |
| 第 10 周 | **Software Factory 与未来**<br>• 可自行运行、自我改进的软件系统<br>• 部署后运行与保护 Agent<br>• AI 软件工程的下一步                                                                                                                   | **12/1（周二）**：Software Factory：可自行运行、自我改进的软件系统<br>**12/3（周四）**：嘉宾（待公布）                                                               |


### Fall 2025


| 周次     | 主题与要点                                                                                                        | 阅读材料                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          | 作业                                                                 | 课程安排                                                                                                                                                                                                                                                                                                                     |
| -------- | ----------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 第 1 周  | **Coding LLM 与 AI 开发导论**<br>• 课程安排<br>• LLM 究竟是什么<br>• 如何有效 prompting                           | <ul><li>[深入理解 LLM](https://www.youtube.com/watch?v=7xTGNNLPyMI) [【中文版】](https://www.bilibili.com/video/BV16cNEeXEer)</li><li>[Prompt Engineering 概览](https://cloud.google.com/discover/what-is-prompt-engineering) [【中文版】](https://www.yuque.com/wangjiandong/gwcyhv/uw3b7we9pmdubdig)</li><li>[Prompt Engineering 指南](https://www.promptingguide.ai/techniques) [【中文版】](https://www.promptingguide.ai/zh/techniques)</li><li>[AI Prompt Engineering：深入解析](https://www.youtube.com/watch?v=T9aRN5JkmL8) [【中文版】](https://www.bilibili.com/video/BV18ukBYzEQG)</li><li>[OpenAI 如何使用 Codex](https://cdn.openai.com/pdf/6a2631dc-783e-479b-b1a4-af0cfbd38630/how-openai-uses-codex.pdf) [【中文版】](https://tools.wingzero.tw/article/sn/3533)</li></ul>                                                                                                                                                                                                        | ✅ 已完成：[LLM Prompting Playground](Assignments/week1/README.md)    | LLM 简介及其构建原理 — [Slides](Resource/Fall2025/week01-0922-intro-to-llms.pptx)<br>LLM 的高效 prompting — [Slides](Resource/Fall2025/week01-0926-effective-prompting.pptx)                                                                                                                                                 |
| 第 2 周  | **Coding Agent 的剖析**<br>• Agent 架构与组件<br>• 工具使用与 function calling<br>• MCP（Model Context Protocol） | <ul><li>[MCP 简介](https://stytch.com/blog/model-context-protocol-introduction/)</li><li>[MCP Server 示例实现](https://github.com/modelcontextprotocol/servers)</li><li>[MCP Server 身份验证](https://developers.cloudflare.com/agents/guides/remote-mcp-server/#add-authentication)</li><li>[MCP Server SDK](https://github.com/modelcontextprotocol/typescript-sdk/tree/main?tab=readme-ov-file#server)</li><li>[MCP Registry](https://blog.modelcontextprotocol.io/posts/2025-09-08-mcp-registry-preview/)</li><li>[关于 MCP 的思考](https://www.reillywood.com/blog/apis-dont-make-good-mcp-tools/)</li></ul>                                                                                                                                                                                                                                                                                                                                                                                 | ✅ 已完成：[AI IDE 初探](Assignments/week2/assignment.md)             | 从零构建 Coding Agent — [Slides](Resource/Fall2025/week02-0929-building-a-coding-agent.pptx)；[已完成练习](Resource/Fall2025/week02-0929-completed-exercise.py)<br>构建自定义 MCP Server — [Slides](Resource/Fall2025/week02-1003-custom-mcp-server.pptx)；[已完成练习](Resource/Fall2025/week02-1003-completed-exercise.py) |
| 第 3 周  | **AI IDE**<br>• 上下文管理与代码理解<br>• 面向 Agent 的 PRD<br>• IDE 集成与扩展                                   | <ul><li>[规格即新的源代码](https://blog.ravi-mehta.com/p/specs-are-the-new-source-code) [【中文版】](https://bbs.sangfor.com.cn/forum.php?mod=viewthread&tid=322197)</li><li>[长上下文如何失效](https://www.dbreunig.com/2025/06/22/how-contexts-fail-and-how-to-fix-them.html)</li><li>[Devin：Coding Agents 101](https://devin.ai/agents101#introduction) [【中文版】](https://www.vibevibe.cn/Articles/01-core-concepts/coding-agents-101.html)</li><li>[让 AI 在复杂代码库中工作](https://github.com/humanlayer/advanced-context-engineering-for-coding-agents/blob/main/ace-fca.md)</li><li>[FAANG 如何 Vibe Code](https://x.com/rohanpaul_ai/status/1959414096589422619)</li><li>[为 Agent 编写有效工具](https://www.anthropic.com/engineering/writing-tools-for-agents) [【中文版】](https://ningto.com/blog/2026/writing-effective-tools-for-agents)</li></ul>                                                                                                                            | ✅ 已完成：[构建自定义 MCP Server](Assignments/week3/assignment.md)   | 从首次 prompt 到最佳 AI IDE 配置 — [Slides](Resource/Fall2025/week03-1006-ai-ide-setup.pptx)；[设计文档模板](Resource/Fall2025/week03-1006-design-document-template.md)<br>Silas Alberti（Cognition 研究负责人）— [Slides](Resource/Fall2025/week03-1010-silas-alberti.pptx)                                                 |
| 第 4 周  | **Coding Agent 模式**<br>• 管理 Agent 的自主性等级<br>• 人机协作模式                                              | <ul><li>[Anthropic 如何使用 Claude Code](https://www-cdn.anthropic.com/58284b19e702b49db9302d5b6f135ad8871e7658.pdf) [【中文版】](https://baoyu.io/translations/how-anthropic-teams-use-claude-code)</li><li>[Claude 最佳实践](https://www.anthropic.com/engineering/claude-code-best-practices) [【中文版】](https://claude.whaty.org/posts/Claude-code-official-best-practices.html)</li><li>[Awesome Claude Agents](https://github.com/vijaythecoder/awesome-claude-agents)</li><li>[Super Claude](https://github.com/SuperClaude-Org/SuperClaude_Framework)</li><li>[好的上下文，好的代码](https://blog.stockapp.com/good-context-good-code/)</li><li>[窥探 Claude Code 的内部机制](https://medium.com/@outsightai/peeking-under-the-hood-of-claude-code-70f5a94a9a62)</li></ul>                                                                                                                                                                                                              | ✅ 已完成：[使用 Claude Code 编程](Assignments/week4/assignment.md)   | 如何成为 Agent 管理者 — [Slides](Resource/Fall2025/week04-1013-agent-manager.pptx)<br>Boris Cherny（Claude Code 创建者）— [Slides](Resource/Fall2025/week04-1017-boris-cherny.pptx)                                                                                                                                          |
| 第 5 周  | **现代终端**<br>• AI 增强的命令行界面<br>• 终端自动化与脚本编写                                                   | <ul><li>[Warp University](https://www.warp.dev/university?slug=university)</li><li>[Warp 与 Claude Code 对比](https://www.warp.dev/university/getting-started/warp-vs-claude-code)</li><li>[Warp 如何用 Warp 构建 Warp](https://notion.warp.dev/How-Warp-uses-Warp-to-build-Warp-21643263616d81a6b9e3e63fd8a7380c)</li></ul>                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      | ✅ 已完成：[使用 Warp 进行 Agentic 开发](Assignments/week5/README.md) | 如何打造一款爆款 AI 开发者产品 — [Slides](Resource/Fall2025/week05-1020-ai-developer-product.pptx)<br>Zach Lloyd（Warp CEO）— [Slides](https://www.figma.com/slides/kwbcmtqTFQMfUhiMH8BiEx/Warp---Stanford--Copy-?node-id=9-116&t=oBWBCk8mjg2l2NR5-1)                                                                        |
| 第 6 周  | **AI 测试与安全**<br>• 安全地 Vibe Coding<br>• 漏洞检测的历史<br>• AI 生成的测试套件                              | <ul><li>[SAST 与 DAST](https://www.splunk.com/en_us/blog/learn/sast-vs-dast.html)</li><li>[通过 Prompt Injection 实现 Copilot RCE](https://embracethered.com/blog/posts/2025/github-copilot-remote-code-execution-via-prompt-injection/) [【中文版】](https://cn-sec.com/archives/5301988.html)</li><li>[使用 Claude Code 与 OpenAI Codex 发现漏洞](https://semgrep.dev/blog/2025/finding-vulnerabilities-in-modern-web-apps-using-claude-code-and-openai-codex/)</li><li>[Agentic AI 威胁：身份欺骗与冒充](https://unit42.paloaltonetworks.com/agentic-ai-threats/)</li><li>[OWASP Top Ten](https://owasp.org/www-project-top-ten/) [【中文版】](https://www.owasp.org.cn/OWASP-CHINA/owasp-project/2021-owasp-top-10/)</li><li>[Context Rot](https://research.trychroma.com/context-rot) [【中文版】](https://research.chroma.org.cn/context-rot)</li><li>[使用 O3 进行漏洞 prompt 分析](https://github.com/SeanHeelan/o3_finds_cve-2025-37899/blob/master/system_prompt_uafs.prompt)</li></ul> | ✅ 已完成：[编写安全的 AI 代码](Assignments/week6/assignment.md)      | AI QA、SAST、DAST 及未来 — [Slides](Resource/Fall2025/week06-1027-ai-qa-sast-dast.pptx)<br>Isaac Evans（Semgrep CEO）                                                                                                                                                                                                        |
| 第 7 周  | **现代软件支持**<br>• 哪些 AI 代码系统值得信任<br>• 调试与诊断<br>• 智能文档生成                                  | <ul><li>[Code Review：做就对了](https://blog.codinghorror.com/code-reviews-just-do-it/)</li><li>[如何有效进行 Code Review](https://github.blog/developer-skills/github/how-to-review-code-effectively-a-github-staff-engineers-philosophy/)</li><li>[现代 Code Review 中 AI 辅助 Coding 实践评估](https://arxiv.org/pdf/2405.13565)</li><li>[AI Code Review 落地最佳实践](https://graphite.dev/guides/ai-code-review-implementation-best-practices)</li><li>[软件团队的 Code Review 要点](https://blakesmith.me/2015/02/09/code-review-essentials-for-software-teams.html)</li><li>[来自数百万次 AI Code Review 的经验](https://www.youtube.com/watch?v=TswQeKftnaw)</li></ul>                                                                                                                                                                                                                                                                                                                    | ✅ 已完成：[Code Review 实践](Assignments/week7/README.md)            | AI Code Review — [Slides](Resource/Fall2025/week07-1103-ai-code-review.pptx)<br>Tomas Reimers（Graphite CPO）— [Slides](Resource/Fall2025/week07-1107-tomas-reimers-slides.pdf)                                                                                                                                              |
| 第 8 周  | **自动化 UI 与应用构建**<br>• 面向所有人的设计与前端开发<br>• 快速 UI/UX 原型与迭代                               | —                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 | ✅ 已完成：[多技术栈 Web 应用构建](Assignments/week8/assignment.md)   | 通过一个 prompt 构建端到端应用 — [Slides](Resource/Fall2025/week08-1110-end-to-end-app.pptx)<br>Gaspar Garcia（Vercel AI 研究负责人）— [Slides](https://docs.google.com/presentation/d/1Jf2aN5zIChd5tT86rZWWqY-iDWbxgR-uynKJxBR7E9E/edit?usp=sharing)                                                                        |
| 第 9 周  | **部署后的 Agent**<br>• AI 系统的监控与可观测性<br>• 自动化事件响应<br>• 分诊与调试                               | <ul><li>[SRE 导论](https://sre.google/sre-book/introduction/)</li><li>[需要了解的可观测性基础](https://last9.io/blog/traces-spans-observability-basics/)</li><li>[使用 AI 排查 Kubernetes 故障](https://resolve.ai/blog/kubernetes-troubleshooting-in-resolve-ai)</li><li>[你的新 Autonomous Teammate](https://resolve.ai/blog/product-deep-dive)</li><li>[多 Agent 系统如何使工程师 AI-native](https://resolve.ai/blog/role-of-multi-agent-systems-AI-native-engineering)</li><li>[Agentic AI 在 On-call 工程中的益处](https://resolve.ai/blog/Top-5-Benefits)</li></ul>                                                                                                                                                                                                                                                                                                                                                                                                                         | —                                                                    | 事件响应与 DevOps — [Slides](Resource/Fall2025/week09-1117-incident-response-devops.pptx)<br>Mayank Agarwal（Resolve CTO）与 Milind Ganjoo（Resolve 技术成员）— [Slides](Resource/Fall2025/week09-1121-resolve-guest-lecture-slides.pdf)                                                                                     |
| 第 10 周 | **AI 软件工程的下一步**<br>• 软件开发角色的未来<br>• 新兴 AI Coding 范式<br>• 行业趋势与预测                      | —                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 | —                                                                    | 十年后的软件开发<br>Martin Casado（a16z 普通合伙人）                                                                                                                                                                                                                                                                         |

## 常见问题
<details>

### 本课程将使用哪些编程语言？

* 本课程不局限于特定的语言，重点是学习适用于不同编程语言的工具和实践。不过，课程示例将主要使用 Python、JavaScript，并在适当情况下使用一些系统编程语言。重点在于理解**现代开发实践**，而非精通特定语言。

### 我是否需要具备使用 GitHub Copilot 等 AI 工具的经验？

* 不需要具备 AI 开发工具的经验。本课程将从基础知识开始，循序渐进地过渡到更高级的应用。然而，扎实的编程基础（相当于 CS111 及以上水平）是必不可少的。

### 本课程会取代传统的软件工程课程吗？

* 本课程是传统软件工程课程的有力补充，重点关注现代工具和 AI 辅助开发。它假定你已具备软件工程的基础知识，并在此基础上教授最新的实践。

### 本课程需要投入多少时间？

* 预计每周投入约 10-12 小时，包括听课、完成作业和项目工作。本课程侧重实践，需要时间来尝试新的工具和技术。

### 是否有特殊的软硬件要求？

* 学生需要使用一台能够运行现代开发工具的计算机。某些基于云的服务可能需要订阅（如 GitHub Copilot 等），但课程将尽可能提供访问权限或替代方案。可靠的互联网连接对于使用基于云的工具至关重要。

### 课程内容的时效性如何？

* 课程内容设计具有高度时效性，将每周更新，以反映 AI 辅助开发这一快速变化的领域。来自行业领先公司的嘉宾讲者将确保学生学到最新的行业实践和新兴工具。

### 我可以旁听本课程吗？

* 我们欢迎斯坦福大学的学生和教职员工申请旁听。旁听者可以参加所有讲座，但我们无法批改您的作业或就期末项目提供建议。

</details>

---


**欢迎加入 动手学CS146S 交流群一起讨论，群内不定期分享由赞助商提供的大模型额度，若群二维码过期请添加个人微信**:
<div align="center">
  <img src="Resource/imgs/group8-21.png" width="20%" height="auto">,<img src="Resource/imgs/personinfo.png" width="20%" height="auto">
</div>



# 许可证

本项目采用 MIT 许可证 - 详情请见 `LICENSE` 文件。
## Star History
<div align="center">
  <img src="Resource/imgs/star-history-2026717.png" width="100%" height="auto">
</div>

[实时数据](https://www.star-history.com/?type=timeline&repos=ShouZhengAI%2FCS146S_CN)
