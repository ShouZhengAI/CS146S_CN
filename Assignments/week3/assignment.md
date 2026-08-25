# 第 3 周——构建自定义 MCP Server

设计并实现一个封装真实外部 API 的模型上下文协议（Model Context Protocol，MCP）Server。你可以：
- 在**本地**运行（使用 STDIO 传输），并将其集成到 MCP 客户端（如 Claude Desktop）中。
- 或者在**远程**运行（使用 HTTP 传输），并通过模型 Agent 或客户端调用。此方式难度更高，但可以获得额外加分。

如果按照 MCP 授权规范添加身份验证（API Key 或 OAuth2），还可获得加分。

## 学习目标
- 理解 MCP 的核心能力：工具（tools）、资源（resources）和提示词（prompts）。
- 使用类型化参数实现工具定义，并提供健壮的错误处理。
- 遵循日志记录和传输的最佳实践（STDIO Server 不得向 stdout 输出内容）。
- 可选择为 HTTP 传输实现授权流程。

## 功能要求
1. 选择一个外部 API，并说明你将使用哪些端点。示例：天气、GitHub Issues、Notion 页面、电影/电视数据库、日历、任务管理器、金融/加密货币、旅行、体育统计数据。
2. 公开至少两个 MCP 工具。
3. 实现基本的容错能力：
   - 妥善处理 HTTP 请求失败、超时和结果为空的情况。
   - 遵守 API 速率限制（例如，采用简单的退避机制或向用户显示警告）。
4. 打包与文档：
   - 提供清晰的安装说明、环境变量配置和运行命令。
   - 给出一个调用流程示例（说明需要在客户端中输入什么或点击什么来触发这些工具）。
5. 选择一种部署模式：
   - 本地：使用 STDIO 的 Server，可在你的计算机上运行，并能被 Claude Desktop 或 Cursor 等 AI IDE 发现。
   - 远程：可通过网络访问的 HTTP Server，能够由支持 MCP 的客户端或 Agent Runtime 调用。如已完成部署并可正常访问，可获得额外加分。
6. （可选）加分项：身份验证
   - 通过环境变量和客户端配置支持 API Key；或者
   - 为 HTTP 传输支持 OAuth2 风格的 Bearer Token，验证 Token Audience，并且绝不将 Token 透传给上游 API。

## 提交物
- `week3/` 目录下的源代码（建议放在 `week3/server/` 中，并提供清晰的入口点，如 `main.py` 或 `app.py`）。
- `week3/README.md`，其中应包含：
  - 前置条件、环境配置和运行说明（本地和/或远程）。
  - 如何配置 MCP 客户端（本地模式以 Claude Desktop 为例），或如何为远程模式配置 Agent Runtime。
  - 工具参考文档：名称、参数、输入/输出示例以及预期行为。

## 评分标准（总计 90 分）
- 功能性（35 分）：实现 2 个或更多工具，正确集成 API，并提供有意义的输出。
- 可靠性（20 分）：输入验证、错误处理、日志记录以及对速率限制的考虑。
- 开发者体验（20 分）：安装与使用文档清晰，易于在本地运行；目录结构合理。
- 代码质量（15 分）：代码易读、命名清晰、复杂度最低，并在适用处使用类型提示。
- 额外加分（10 分）：
  - +5 分：远程 HTTP MCP Server，可由 OpenAI/Claude SDK 等 Agent 或客户端调用。
  - +5 分：正确实现身份验证（API Key，或带有 Audience 验证的 OAuth2）。

## 相关参考链接
- MCP Server 快速入门：[modelcontextprotocol.io/quickstart/server](https://modelcontextprotocol.io/quickstart/server)。 
*注意：不得直接提交此示例。*
- MCP 授权（HTTP）：[modelcontextprotocol.io/specification/2025-06-18/basic/authorization](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization)
- Cloudflare 上的远程 MCP（Agents）：[developers.cloudflare.com/agents/guides/remote-mcp-server/](https://developers.cloudflare.com/agents/guides/remote-mcp-server/)。部署前，请使用 Model Context Protocol Inspector 工具在本地调试你的 Server。
- 如果选择部署远程 MCP，可以使用 [Vercel](https://vercel.com/docs/mcp/deploy-mcp-servers-to-vercel)；它提供免费套餐，是一个不错的选择。