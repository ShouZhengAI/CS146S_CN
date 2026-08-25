# 第 3 周：GitHub MCP Server

这是一个封装 GitHub REST API 的 MCP Server，支持：

- STDIO：供 Claude Desktop、Cursor 等本地客户端启动。
- Streamable HTTP：默认地址 `http://127.0.0.1:8000/mcp`。
- HTTP/SSE：SSE 地址 `http://127.0.0.1:8000/sse`，消息端点由 MCP SDK 管理。
- 4 个工具、3 个资源、2 个提示词。
- API Key 或带签名、过期时间和 Audience 校验的 OAuth Bearer JWT。
- 超时、并发限制、指数退避、GitHub 限流提示和结构化错误。

## 目录

```text
week3/
├── requirements.txt
└── server/
    ├── __init__.py
    ├── auth.py       # HTTP API Key/JWT 验证
    ├── config.py     # 环境变量与启动配置
    ├── github.py     # GitHub API、重试、限流处理
    └── main.py       # MCP 工具、资源、提示词和传输入口
```

## 前置条件与安装

- Python 3.11 或更高版本。
- 可访问 `https://api.github.com`。
- 只读公开仓库可以不设置 GitHub Token，但匿名限额较低。
- 创建/修改 Issue 必须使用具有目标仓库 `Issues: Read and write` 权限的 fine-grained GitHub Token。

在仓库根目录执行：

```bash
cd assignments/week3
python -m venv .venv
source .venv/bin/activate       # Windows: .venv\Scripts\activate
python -m pip install -r requirements.txt
```

## 环境变量

| 变量 | 默认值 | 说明 |
|---|---|---|
| `GITHUB_TOKEN` | 空 | 上游 GitHub Token，只发给 GitHub，不会使用客户端的 MCP Token |
| `GITHUB_API_URL` | `https://api.github.com` | GitHub REST API 根地址，也可指向 GitHub Enterprise |
| `GITHUB_API_VERSION` | `2022-11-28` | GitHub API 版本 |
| `GITHUB_USER_AGENT` | `cs146s-week3-mcp/1.0` | 上游请求 User-Agent |
| `REQUEST_TIMEOUT_SECONDS` | `15` | 单次上游请求超时 |
| `MAX_RETRIES` | `3` | 失败后的最大重试次数，可设为 `0` |
| `MAX_CONCURRENCY` | `8` | 同时进行的 GitHub 请求上限 |
| `MCP_TRANSPORT` | `stdio` | `stdio`、`sse` 或 `streamable-http` |
| `MCP_HOST` | `127.0.0.1` | HTTP 监听地址；公网部署时可设 `0.0.0.0` |
| `MCP_PORT` | `8000` | HTTP 监听端口 |
| `MCP_AUTH_MODE` | `none` | `none`、`api-key`、`bearer` 或 `either` |
| `MCP_API_KEY` | 空 | `api-key`/`either` 模式下必填，客户端放入 `X-API-Key` |
| `MCP_JWT_SECRET` | 空 | HS256/384/512 JWT 密钥；和 `MCP_JWKS_URL` 二选一 |
| `MCP_JWKS_URL` | 空 | RS/ES JWT 的 JWKS 地址；推荐生产环境使用 |
| `MCP_JWT_AUDIENCE` | 空 | Bearer 模式必填，JWT 的 `aud` 必须匹配 |
| `MCP_JWT_ISSUER` | 空 | 可选；设置后 JWT 的 `iss` 也必须匹配 |
| `LOG_LEVEL` | `INFO` | 日志级别 |

示例：

```bash
export GITHUB_TOKEN="github_pat_..."
export REQUEST_TIMEOUT_SECONDS=20
export MAX_RETRIES=3
```

不要把 Token 写入 Git、README 或 MCP 提示词。日志只写 stderr；STDIO 的 stdout 始终留给 MCP JSON-RPC。

## 启动

所有命令均在 `week3/` 目录执行。

### STDIO

```bash
python -m server.main --transport stdio
```

STDIO Server 通常由 MCP 客户端启动，不需要手工保持终端运行。

### Streamable HTTP

```bash
MCP_TRANSPORT=streamable-http MCP_HOST=127.0.0.1 MCP_PORT=8000 \
python -m server.main
```

客户端 URL：`http://127.0.0.1:8000/mcp`。

### HTTP/SSE

```bash
MCP_TRANSPORT=sse MCP_HOST=127.0.0.1 MCP_PORT=8000 \
python -m server.main
```

客户端 SSE URL：`http://127.0.0.1:8000/sse`。

命令行 `--transport` 的优先级高于 `MCP_TRANSPORT`。

## 远程认证

认证只用于 HTTP/SSE，STDIO 依赖本机进程权限。

### API Key

```bash
export MCP_AUTH_MODE=api-key
export MCP_API_KEY='生成的高熵随机值'
python -m server.main --transport streamable-http
```

客户端每个请求发送：

```http
X-API-Key: 生成的高熵随机值
```

### OAuth 风格 Bearer JWT

使用 JWKS 的推荐配置：

```bash
export MCP_AUTH_MODE=bearer
export MCP_JWKS_URL='https://login.example.com/.well-known/jwks.json'
export MCP_JWT_AUDIENCE='https://mcp.example.com'
export MCP_JWT_ISSUER='https://login.example.com/'
python -m server.main --transport streamable-http
```

开发环境也可设置 `MCP_JWT_SECRET` 验证 HS256 JWT。Server 会验证签名、`exp`、`aud`，设置 Issuer 后还验证 `iss`。`either` 模式允许 API Key 或 Bearer 二选一。客户端的 Bearer/API Key 只在本 Server 校验，绝不会透传给 GitHub；GitHub 只接收独立的 `GITHUB_TOKEN`。

## Claude Desktop 配置

编辑 Claude Desktop 配置文件（macOS：`~/Library/Application Support/Claude/claude_desktop_config.json`）。把路径替换为自己的绝对路径：

```json
{
  "mcpServers": {
    "github-operations": {
      "command": "/绝对路径/assignments/week3/.venv/bin/python",
      "args": ["-m", "server.main", "--transport", "stdio"],
      "cwd": "/绝对路径/assignments/week3",
      "env": {
        "GITHUB_TOKEN": "github_pat_...",
        "LOG_LEVEL": "INFO"
      }
    }
  }
}
```

保存后完全退出并重启 Claude Desktop。在工具列表中应看到 `search_github_issues` 等 4 个工具。Token 更适合由启动脚本或系统密钥管理器注入，不建议长期明文保存在配置文件。

## Cursor 配置

项目内创建 `.cursor/mcp.json`：

```json
{
  "mcpServers": {
    "github-operations": {
      "command": "/绝对路径/assignments/week3/.venv/bin/python",
      "args": ["-m", "server.main", "--transport", "stdio"],
      "cwd": "/绝对路径/assignments/week3",
      "env": {
        "GITHUB_TOKEN": "github_pat_..."
      }
    }
  }
}
```

若 Cursor 版本支持远程 MCP，可改为：

```json
{
  "mcpServers": {
    "github-operations-remote": {
      "url": "https://mcp.example.com/mcp",
      "headers": {
        "Authorization": "Bearer <JWT>"
      }
    }
  }
}
```

不同 Cursor 版本对远程 MCP 字段支持可能不同；STDIO 配置最稳定。

## 工具参考

所有工具都返回 JSON。成功时 `ok` 为 `true`；失败时返回 `{"ok": false, "error": {"type", "message", "status_code"}}`。自动重试或空结果等非致命情况位于 `meta.warnings` 或 `warnings`。

### 1. `search_github_issues`

使用 GitHub Issue 搜索语法搜索 Issue 和 Pull Request。

| 输入 | 类型 | 说明 |
|---|---|---|
| `query` | string，必填 | 最长 256 字符，如 `repo:octocat/Hello-World is:issue is:open bug` |
| `sort` | enum | `created`/`updated`/`comments`/`reactions`/`interactions`，默认 `updated` |
| `order` | `asc`/`desc` | 默认 `desc` |
| `page` | 1..1000 | 默认 1 |
| `per_page` | 1..100 | 默认 20 |

调用示例：

```json
{"query":"repo:octocat/Hello-World is:issue is:open","sort":"updated","per_page":5}
```

输出包含 `total_count`、`incomplete_results`、精简后的 `items` 和重试信息。无匹配项不是错误，会返回空数组和 warning。

### 2. `get_github_issue`

读取单个 Issue 或 Pull Request 的正文与元数据。

```json
{"owner":"octocat","repo":"Hello-World","issue_number":1347}
```

输出包含仓库名、标题、正文、状态、标签、负责人、评论数、时间和网页 URL。GitHub 对 Issue/PR 共用此端点，`kind` 会明确类型。

### 3. `create_or_update_github_issue`

创建或更新 Issue。该工具会产生外部写操作，客户端应在调用前让用户确认目标仓库和内容。

| 输入 | 类型 | 说明 |
|---|---|---|
| `owner`, `repo` | string，必填 | 目标仓库 |
| `issue_number` | integer，可选 | 不提供表示创建；提供表示更新 |
| `title` | string | 创建时必填，更新时可选 |
| `body` | string | 最长 65536 字符 |
| `labels` | string[] | 最多 20 个；标签必须已存在，否则 GitHub 可能拒绝 |
| `assignees` | string[] | 最多 10 个 |
| `state` | `open`/`closed` | 仅在需要变更状态时提供 |

创建：

```json
{
  "owner":"my-org",
  "repo":"my-repo",
  "title":"文档中的安装命令失效",
  "body":"复现步骤：...",
  "labels":["documentation"]
}
```

更新：

```json
{"owner":"my-org","repo":"my-repo","issue_number":42,"state":"closed"}
```

输出的 `action` 为 `created` 或 `updated`，并返回 GitHub 最终保存的 Issue。创建缺少标题、更新没有任何字段会直接返回校验错误，不请求 GitHub。

### 4. `summarize_github_repository`

并行读取仓库信息、语言、前 5 位贡献者和最新 Release，生成确定性的概览，不调用额外的生成式 AI。

```json
{"owner":"modelcontextprotocol","repo":"python-sdk"}
```

输出包含描述、默认分支、许可证、主题、Star/Fork/Open Issue 数量、语言占比、主要贡献者和最新 Release。可选端点失败时保留其余结果并给出 warning；仓库主信息失败时返回错误。

## 资源参考

| URI | 内容 |
|---|---|
| `github://api/schema` | 本 Server 实际使用的 GitHub REST 端点和 API 版本 |
| `service://status` | GitHub 是否配置 Token、最近一次成功时间、请求数和最近的限流快照 |
| `service://logs` | 最近 100 条内存日志，进程重启即清空；凭据不会记录 |

资源调用没有输入。例如读取 `service://status` 可检查 `rate_limit.remaining`，无需额外请求 GitHub。状态值在第一次上游调用前可能为 `null`，这是“尚未观察到”，不是故障。

## 提示词参考

### `analyze_github_bug`

输入：`owner`、`repo`、`issue_number`，可选 `focus`。它要求模型先读 Issue，再区分事实和假设，输出复现、根因、最小修复与验证计划。

```json
{"owner":"my-org","repo":"my-repo","issue_number":42,"focus":"并发条件下的数据丢失"}
```

### `draft_feature_spec`

输入：`owner`、`repo`、`feature`，可选 `audience`。它要求模型先读取仓库概览并搜索相关 Issue，再写带非目标、失败情况、安全、迁移和验收标准的功能规格。

```json
{"owner":"my-org","repo":"my-repo","feature":"为 CLI 增加 JSON 输出"}
```

## 完整调用流程示例

1. 在客户端输入：“搜索 `modelcontextprotocol/python-sdk` 里最近更新的 5 个 open bug，只列出标题和链接。”
2. 客户端应选择 `search_github_issues`，参数为：

   ```json
   {"query":"repo:modelcontextprotocol/python-sdk is:issue is:open label:bug","sort":"updated","per_page":5}
   ```

3. 再输入：“读取其中第一个 Issue，并按 bug 分析模板给出排查计划。”
4. 客户端读取 `analyze_github_bug` 提示词，并调用 `get_github_issue`。
5. 若要求创建 Issue，先核对仓库、标题和正文；用户确认后再调用写工具。

## 错误处理与限流

- 参数先由类型和范围规则校验，非法 owner、页码、超长正文不会到达 GitHub。
- 网络错误、超时、HTTP 429 和临时 5xx 使用指数退避并加入随机抖动。
- GitHub 返回 `Retry-After` 或 `X-RateLimit-Reset` 时优先遵守，单次等待最多 60 秒。
- GitHub 401、404、限流 403 会转换为短且可执行的错误，不返回 Token 或原始响应头。
- 并发请求由信号量限制，避免摘要工具瞬间打满上游。
- 摘要的次要请求允许局部失败；核心仓库请求失败则整体失败。
- GitHub 搜索为空时返回成功和 warning，客户端不需要用异常表达“没有结果”。

## 解题思路与设计理由

### 任务 1：外部 API 与多端点

选择 GitHub 是因为搜索、读取、写入和汇总都能用真实端点完成。API 访问集中在 `github.py`，MCP 层只做参数校验和结果整理，后续换 GitHub Enterprise 只需改环境变量。

### 任务 2：4 个丰富工具

工具按“搜索、读取、写入、汇总”划分，每个职责清楚。创建和更新共享一个入口，但用 `issue_number` 明确动作，避免重复代码。返回统一的 `ok/error` 结构，模型容易判断下一步。

### 任务 3：资源与提示词

Schema、状态和日志适合反复读取，所以做成资源，不做成工具。Bug 分析和功能规格是可复用工作流，所以做成提示词；提示词要求先取证，减少模型凭空猜测。

### 任务 4：可靠性

请求失败不立刻报错：先看 GitHub 限流头，再按指数退避重试。摘要允许非核心数据失败，避免“没有 Release”导致整份摘要不可用。所有参数有类型和边界，错误在靠近输入的位置暴露。

### 任务 5：两种传输

同一套工具注册给 STDIO、SSE 和 Streamable HTTP，避免三份实现。STDIO 日志只写 stderr，不破坏 JSON-RPC；远程模式交给 ASGI/Uvicorn，适合反向代理部署。

### 任务 6：认证与安全

HTTP 认证放在 MCP 应用外层，所有 MCP 路径统一保护。API Key 用常量时间比较；JWT 固定允许算法并校验签名、过期时间和 Audience。MCP 凭据与 GitHub Token 完全分离，防止把客户端 Token 泄露给上游。
