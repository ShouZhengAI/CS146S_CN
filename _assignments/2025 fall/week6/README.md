# 第 6 周：用 Semgrep 修复安全问题

## 安全架构

```text
浏览器
  │  同源请求；DOM 只写文本
  ▼
FastAPI
  ├─ TrustedHost：只接受允许的 Host
  ├─ CORS：只允许明确来源、方法和请求头
  ├─ SlowAPI：每个客户端默认 60 次/分钟
  ├─ Security Headers：CSP、HSTS、nosniff、DENY frame 等
  ├─ Pydantic：限制输入长度
  ▼
SQLAlchemy ORM
  ├─ 绑定查询参数
  ├─ 排序字段白名单
  ▼
SQLite
```

配置由环境变量提供：

- `CORS_ORIGINS`：逗号分隔的可信来源；禁止 `*`。默认仅本机 8000 端口。
- `ALLOWED_HOSTS`：逗号分隔的可信 Host。默认 `localhost,127.0.0.1,testserver`。
- `RATE_LIMIT`：SlowAPI 格式，如 `60/minute`。
- `DATABASE_PATH`：SQLite 文件路径。

源码不保存令牌。需要真实密钥时，应通过部署环境或密钥管理服务注入。

## Semgrep 扫描

在仓库根目录执行：

```bash
semgrep ci --subdir week6
```

扫描范围包括：

- `week6/backend/`：Python/FastAPI SAST；
- `week6/frontend/`：JavaScript DOM XSS；
- `week6/`：密钥；
- `week6/requirements.txt`：第三方依赖风险。

查看每条结果的规则 ID、污点来源和危险写入点。修复后重复同一命令，确认旧结果消失且没有新增高危结果。依赖扫描要同时记录升级前后版本，不能只忽略告警。

## 问题分析与解题思路

### 1. SQL 注入

**问题**：旧搜索接口把 `q` 拼进 SQL，输入可能变成 SQL 语法。运行时还用 `text()` 执行种子 SQL。

**思路**：用 `select(Note)`、`.where()`、`.contains()` 和 ORM 写入。SQLAlchemy 自动绑定输入；排序只从固定列字典选择。不要自己加引号或手动转义 SQL。

### 2. XSS / DOM 注入

**问题**：标题和正文来自用户，写入 `innerHTML` 后会被浏览器当成标签解析。

**思路**：结构用 `createElement` 创建，用户数据只进 `textContent` 或 `createTextNode`。清空列表用 `replaceChildren()`。再用 CSP 限制脚本来源，形成双层防护。

### 3. CORS、限流与响应头

**问题**：通配来源、方法和请求头扩大跨站调用范围；没有限流时，一个客户端可持续消耗数据库和应用资源。

**思路**：来源、Host、方法、请求头都用允许列表；拒绝 `CORS_ORIGINS=*`；用 SlowAPI 设置每 IP 默认限额；增加 CSP、HSTS、`nosniff`、`DENY` frame、Referrer Policy 和 Permissions Policy。

### 4. 硬编码密钥与危险调试接口

**问题**：仓库中的令牌会进入提交历史；MD5、`eval`、shell、任意 URL 请求和任意文件读取接口可导致碰撞攻击、代码执行、命令注入、SSRF 或文件泄露。

**思路**：未使用的密钥和调试接口直接删除，不做“隐藏路由”。真实密钥只从环境或密钥服务读取。密码应使用 Argon2/bcrypt/scrypt；普通完整性摘要至少用 SHA-256。

### 5. 依赖漏洞

**问题**：原依赖版本长期未维护，包含多个公开漏洞，也与代码使用的 Pydantic 2 API 不匹配。

**思路**：升级到仍受维护的精确版本并保留锁定，加入实际使用的 `python-dotenv` 和 `slowapi`。SCA 告警要通过升级根依赖解决，不用关闭规则掩盖问题。

## 关键文件

- `backend/app/routers/notes.py`：参数化查询和排序白名单。
- `backend/app/db.py`：ORM 种子数据。
- `backend/app/main.py`：CORS、可信 Host、限流和安全响应头。
- `backend/app/schemas.py`：请求长度边界。
- `frontend/app.js`：安全 DOM 写入。
- `requirements.txt`：已修补并锁定的依赖。
- `writeup.md`：发现、规则 ID、风险、差异和缓解说明。
