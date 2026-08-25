# 第 6 周作业报告

## 提交信息

姓名：**未提供**  
SUNet ID：**未提供**  
引用资料：[Semgrep 文档](https://semgrep.dev/docs/)、[SQLAlchemy ORM 查询指南](https://docs.sqlalchemy.org/en/20/orm/queryguide/)、[OWASP XSS Prevention Cheat Sheet](https://owasp.org/www-community/xss-prevention-cheatsheet)、[FastAPI CORS 文档](https://fastapi.tiangolo.com/tutorial/cors/)

本次作业用时：**未记录**。

## 简要的发现概述

- **SAST**：发现 SQL 字符串插值、`innerHTML` DOM 注入、通配 CORS、MD5、`eval`、shell 命令执行、可控 URL 请求和任意文件读取。前三类可直接造成注入或扩大攻击面；危险调试接口全部删除，而不是只隐藏。
- **密钥扫描**：`backend/app/services/extract.py` 中有硬编码的 Stripe 风格令牌；已删除，代码不再保存密钥。以后需要凭据时只从环境变量或密钥管理服务读取。
- **SCA**：`requirements.txt` 原来的 FastAPI、Uvicorn、SQLAlchemy、Pydantic、Requests、PyYAML、Jinja2、MarkupSafe 和 Werkzeug 均明显过旧。已升级并精确锁定到维护版本，同时增加 `python-dotenv` 和限流组件 `slowapi`。
- **噪声研判**：`data/seed.sql` 只有仓库内固定的初始化数据，没有接收外部输入，不构成 SQL 注入；不过运行时代码已改用 ORM 写入种子数据。`list.replaceChildren()` 只清空已有节点，不解析 HTML，也不是 XSS sink。

## 修复项 1：SQL 注入

a. **文件及行号**  
`backend/app/routers/notes.py:26-42`；`backend/app/db.py:42-68`。

b. **Semgrep 标记的规则/类别**  
`python.sqlalchemy.security.audit.avoid-sqlalchemy-text.avoid-sqlalchemy-text`，类别为 CWE-89（SQL Injection）。

c. **风险说明**  
原搜索接口把查询参数 `q` 直接放进 `text(f"...{q}...")`。攻击者可闭合字符串并改变 `WHERE` 条件，读取非预期数据，甚至在支持多语句的驱动中修改数据。

d. **修改与 AI 工具使用**  
使用 AI 辅助定位数据流并核对所有数据库调用，随后逐处人工检查。

```diff
- sql = text(f"SELECT ... WHERE title LIKE '%{q}%' OR content LIKE '%{q}%'")
- rows = db.execute(sql).all()
+ stmt = select(Note).where(
+     Note.title.contains(q) | Note.content.contains(q)
+ )
+ rows = db.execute(stmt.offset(skip).limit(limit)).scalars().all()
```

同时将排序字段改成显式列白名单，并把 `seed.sql` 的运行时执行改成 `select(...)` 与 `session.add_all(...)`，删除后端中的动态 SQL 和 `text()`。

e. **缓解原因**  
SQLAlchemy 表达式把 `q` 作为绑定参数传给数据库，输入只会被当作值，不会成为 SQL 语法；排序白名单也阻止用户选择任意模型属性。

## 修复项 2：XSS / DOM 注入

a. **文件及行号**  
`frontend/app.js:7-18,21-28`；`frontend/index.html:20,33,40`。

b. **Semgrep 标记的规则/类别**  
`javascript.browser.security.insecure-document-method.insecure-document-method`（DOM XSS / CWE-79）。

c. **风险说明**  
标题和正文由用户创建。原代码用模板字符串写入 `li.innerHTML`，如 `<img src=x onerror=...>` 会被浏览器解析为标签并执行事件处理器，从而窃取页面数据或以用户身份调用 API。

d. **修改与 AI 工具使用**  
使用 AI 辅助检查所有 DOM 写入点，保留节点结构但取消 HTML 解析。

```diff
- list.innerHTML = '';
- li.innerHTML = `<strong>${n.title}</strong>: ${n.content}`;
+ list.replaceChildren();
+ const title = document.createElement('strong');
+ title.textContent = n.title;
+ li.append(title, document.createTextNode(`: ${n.content}`));
```

`index.html` 的内联样式移到 `styles.css`，脚本改为 `defer`，从而允许严格 CSP 禁止内联脚本和样式。

e. **缓解原因**  
`textContent` 和 `createTextNode` 不解析 HTML；尖括号、事件属性和 `<script>` 都只显示为普通文本。CSP 又提供第二层防护，即使未来误加 sink，也会限制内联脚本执行。

## 修复项 3：平台配置、密钥与弱安全接口

a. **文件及行号**  
`backend/app/main.py:27-80`；原 `backend/app/routers/notes.py:69-131`（危险路由已删除，修复后文件止于第 74 行）；原 `backend/app/services/extract.py:13`（硬编码令牌已删除，修复后文件止于第 10 行）；`requirements.txt:1-11`。

b. **Semgrep 标记的规则/类别**  
`python.fastapi.security.wildcard-cors.wildcard-cors`、`generic.secrets.security.detected-stripe-api-key.detected-stripe-api-key`、`python.lang.security.insecure-hash-algorithms.insecure-hash-algorithm-md5`、`python.lang.security.audit.eval-detected.eval-detected`，以及 SCA 依赖告警。

c. **风险说明**  
`allow_origins=["*"]` 配合凭据会让任意站点跨域调用服务；无限请求可造成资源耗尽；源码密钥会随仓库永久泄露；MD5 不抗碰撞；`eval`、shell、任意 URL 和任意路径调试接口分别带来代码执行、命令注入、SSRF 和文件泄露。旧依赖还包含公开漏洞。

d. **修改与 AI 工具使用**  
使用 AI 辅助整理 Semgrep 结果和中间件配置，人工确认默认值为最小权限。

```diff
- allow_origins=["*"]
- allow_credentials=True
- allow_methods=["*"]
- allow_headers=["*"]
+ allow_origins=cors_origins
+ allow_credentials=False
+ allow_methods=["GET", "POST", "PATCH", "PUT", "OPTIONS"]
+ allow_headers=["Accept", "Content-Type"]
```

新增每 IP 默认 `60/minute` 的 SlowAPI 限流、可信 Host 校验、CSP/HSTS（仅 HTTPS）、`nosniff`、拒绝嵌套、Referrer 和 Permissions Policy。`CORS_ORIGINS`、`ALLOWED_HOSTS`、`RATE_LIMIT` 从环境读取，且显式拒绝通配来源。删除硬编码令牌及全部危险调试路由；依赖升级为 FastAPI 0.116.1、Uvicorn 0.35.0、SQLAlchemy 2.0.41、Pydantic 2.11.7、Requests 2.32.4、PyYAML 6.0.2、Jinja2 3.1.6、MarkupSafe 3.0.2、Werkzeug 3.1.3。

e. **缓解原因**  
来源、方法、请求头和 Host 都采用允许列表；限流约束单个客户端消耗；响应头降低脚本注入、MIME 嗅探、点击劫持和信息外泄风险。删除未使用的密钥和高危接口从根源上移除攻击面，升级锁定版本则消除旧版本已知漏洞并保证安装可复现。
