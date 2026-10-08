# 第 7 周：笔记与行动项服务

这是一个 FastAPI + SQLAlchemy + SQLite 的小型全栈项目。后端提供笔记、行动项和标签 API；静态前端可创建、搜索、完成和删除数据。

## 功能

- 笔记与行动项完整 CRUD
- 严格 Pydantic 校验和统一的 400/404/422 错误响应
- `skip`/`limit` 分页、字段白名单排序和组合筛选
- 标签模型及笔记—标签多对多关系
- 行动项结构化提取：日期、优先级、负责人、标签、复选框状态
- 无 Node 构建步骤的静态前端

## 目录

```text
backend/app/                 FastAPI 应用、模型、路由和提取服务
backend/tests/               API、提取、分页与排序测试
frontend/                    HTML、CSS 和浏览器端 JavaScript
data/                        SQLite 数据和种子 SQL
docs/TASKS.md                作业任务
writeup.md                   实现与审查报告
```

## 快速开始

在仓库根目录安装开发依赖，然后进入本周目录：

```bash
pip install -e .[dev]
cd assignments/week7
make run
```

访问：

- 前端：`http://localhost:8000`
- OpenAPI 文档：`http://localhost:8000/docs`

默认数据库为 `./data/app.db`。可通过环境变量 `DATABASE_PATH` 指定其他路径。

## API 概览

| 资源 | 接口 |
|---|---|
| 笔记 | `GET/POST /notes/`，`GET/PATCH/DELETE /notes/{id}` |
| 行动项 | `GET/POST /action-items/`，`GET/PATCH/DELETE /action-items/{id}`，`PUT /action-items/{id}/complete` |
| 标签 | `GET/POST /tags/`，`GET/DELETE /tags/{id}` |

笔记列表支持 `q`、`tag`、`skip`、`limit`、`sort`；行动项列表支持 `completed`、`q`、`skip`、`limit`、`sort`。排序前加 `-` 表示降序，例如 `sort=-created_at`。

笔记创建示例：

```json
{
  "title": "发布计划",
  "content": "周五前完成检查",
  "tags": ["work", "release"]
}
```

错误响应结构：

```json
{
  "error": {
    "status": 422,
    "message": "Request validation failed",
    "details": []
  }
}
```

## 行动项提取

`extract_action_item_details(text, today=...)` 返回结构化结果。支持：

- `[ ]`、`[x]` 复选框
- `TODO:`、`ACTION:`、常见祈使动词和句末 `!`
- `@high`、`@low` 优先级
- `@alice` 负责人和 `#work` 标签
- `2026-09-01`、`08/30/2026`、`tomorrow`、`next week`、`by Friday`

旧接口 `extract_action_items(text)` 仍返回描述字符串列表。

## 四项任务的解题思路

### 任务 1：端点与验证

先补齐单条读取和删除，让两类资源都形成 CRUD。校验统一放在 Pydantic 模型和 Query 约束中；异常处理器只负责把 400、404、422 转成同一响应格式，避免每个路由重复判断。

### 任务 2：扩展提取

先用正则拆出复选框和显式标记，再用少量动词做行动句启发式判断。日期统一转成 ISO；`today` 可注入，保证相对日期可稳定测试。优先级标记从负责人候选中排除。

### 任务 3：新模型与关系

用联结表实现笔记和标签的多对多关系。创建或更新笔记时按名称复用标签，不存在才新增；查询用 `selectin` 预取标签，避免逐条查询。

### 任务 4：分页与排序测试

准备顺序明确、筛选结果可区分的数据，分别验证空页、越界页、首页/末页、升降序和非法参数。再组合两个筛选条件，防止实现误用 OR。排序追加 `id` 作为次级键，保证翻页稳定。

## 测试与检查

```bash
make test
make lint
make format
```

