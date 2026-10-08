# 第 5 周：智能体驱动的全栈开发

这是一个 FastAPI + SQLAlchemy + SQLite 笔记应用。当前版本完成任务 2–8，并提供 Warp Drive 规则、工作流和多智能体提示词。

## 架构

```text
frontend/                    原生 HTML/CSS/JS；搜索、分页、筛选、标签、乐观更新
backend/app/main.py          FastAPI 入口、静态资源、统一异常封装
backend/app/models.py        Note、ActionItem、Tag、note_tags
backend/app/schemas.py       Pydantic 输入验证和响应结构
backend/app/routers/         notes、action-items、tags API
backend/app/services/        hashtag 与 checkbox 提取
backend/tests/               API、关系、事务、错误和提取测试
.warp/workflows/             可复用 Warp Drive 工作流
.warp/rules/                 项目级工程规则
.warp/prompts/               多智能体角色与交接策略
```

所有 API 成功时返回 `{ "ok": true, "data": ... }`；失败时返回 `{ "ok": false, "data": null, "error": { "code": ..., "message": ... } }`。集合的 `data` 包含 `items`、`total`、`page`、`page_size`。

## 安装与运行

在仓库根目录安装依赖，然后从 `week5/` 启动：

```bash
pip install -e .[dev]
cd week5
make run
```

打开 `http://localhost:8000` 使用界面，打开 `http://localhost:8000/docs` 查看 API。默认数据库是 `week5/data/app.db`；可在 `.env` 中用 `DATABASE_PATH` 覆盖。

## 测试与代码检查

```bash
cd week5
make test
make lint
make format
```

测试使用临时 SQLite 数据库，不会修改应用数据库。

## 主要接口

- `GET /notes/?page=1&page_size=10&tag=python`
- `GET /notes/search?q=api&page=1&page_size=10&sort=created_desc|title_asc`
- `POST /notes/`、`GET/PUT/DELETE /notes/{id}`
- `POST /notes/{id}/extract?apply=true`
- `GET /action-items/?completed=false&page=1&page_size=10`
- `POST /action-items/bulk-complete`
- `GET/POST /tags/`、`DELETE /tags/{id}`
- `POST /notes/{id}/tags`、`DELETE /notes/{id}/tags/{tag_id}`

## Warp Drive 使用

在 Warp Drive 中导入 `.warp/workflows/`。`week5-agent-handoff` 生成带角色、文件范围和接口契约的代理交接包；`week5-api-review` 统一检查响应、验证、分页和事务。`.warp/rules/week5-engineering.md` 可保存为项目规则，`.warp/prompts/multi-agent-playbook.md` 给出协调者、后端、前端、测试和审查提示词。

## 各任务解题思路

1. **Vite + React**：先固定 API 契约，再把列表、表单和分页拆成组件；构建产物统一放到 `dist`，由 FastAPI 提供。当前实现保留轻量原生前端，本次范围未迁移 React。
2. **搜索、排序、分页**：SQLAlchemy 共用同一筛选条件做 `count` 和数据查询；文本转小写匹配，排序值用枚举限制，最后 `offset + limit`。
3. **笔记 CRUD 与乐观更新**：Pydantic 拦截空白和超长文本；界面先保存旧状态再更新，接口失败就回滚。
4. **待办筛选与批量完成**：布尔查询参数直接追加条件；批量操作先确认所有 ID 存在，再统一修改，避免部分成功。
5. **标签多对多**：用 `note_tags` 连接表关联笔记和标签；标签统一去掉 `#`、转小写并保持唯一，重复关联保持幂等。
6. **内容提取**：正则识别 `#hashtags` 和 `- [ ] task`；保持原顺序去重，`apply=true` 时在同一请求中写入标签和待办。
7. **错误与响应封装**：全局处理 HTTP、验证和未知异常；错误只返回稳定代码和安全消息，前端只消费统一 envelope。
8. **集合分页**：页码从 1 开始，页大小限制为 1–100；总数单独查询，超出最后一页返回空 `items` 而不是报错。
9. **查询性能与索引**：在标题、创建时间、完成状态、标签名和连接表外键上建索引；大数据量时用 SQLite 查询计划确认索引命中。
10. **测试覆盖**：按可观察行为覆盖成功、422、404、409、分页边界、关系幂等、提取持久化和事务回滚，不测试内部实现文本。
11. **Vercel 部署**：React 构建输出交给 Vercel，API 用 Python 函数或独立服务；通过环境变量注入 API 地址，发布前保留上一版本用于回滚。本次范围未加入部署配置。
