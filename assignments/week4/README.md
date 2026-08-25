# Week 4：开发者指挥中心

这是一个 FastAPI、SQLite 和原生 JavaScript 组成的笔记/行动项应用。后端提供笔记 CRUD、搜索和行动项完成接口；前端可以新增、搜索、编辑、删除笔记，并完成行动项。

## 目录

- `backend/app/routers/`：HTTP 路由
- `backend/app/schemas.py`：请求校验和响应结构
- `backend/app/services/extract.py`：行动项、标签提取
- `backend/tests/`：接口和服务测试
- `frontend/`：页面、样式和交互
- `docs/API.md`：API 契约
- `.claude/commands/`：可复用的 Claude 工作流
- `CLAUDE.md`：仓库级开发规则

## 使用

在 `week4/` 目录运行：

```bash
conda activate cs146s
make run
```

打开 `http://127.0.0.1:8000`。常用检查：

```bash
make test
make lint
make format
pre-commit run --all-files
```

Claude 自定义命令：

```text
/tests backend/tests/test_notes.py
/docs-sync http://127.0.0.1:8000
/refactor-module backend/app/services/old.py backend/app/services/new.py
```

## 各任务解题思路

### 1. pre-commit

把 Black 和 Ruff 放进提交前钩子。先自动格式化，再检查剩余问题，避免风格错误进入提交。

### 2. 笔记搜索

固定路由 `/notes/search` 放在 `/{note_id}` 前。用 SQLAlchemy `ilike` 同时匹配标题和正文，查询值用参数绑定，不拼 SQL。前端用 `encodeURIComponent` 编码关键词。

### 3. 完成行动项

按 ID 查询；不存在返回 404，存在则把 `completed` 设为 `true`。重复调用结果不变，前端完成后重新加载列表。

### 4. 标签提取

正则只识别独立的 `#标签`，支持字母、数字、下划线、连字符和 Unicode；按出现顺序去重。行动项提取保持原接口，`extract_note` 一次返回行动项和标签。

### 5. 笔记 CRUD

`PUT` 先查记录，再同时替换标题和正文；`DELETE` 删除后返回 204 空响应。前端按钮调用对应接口，成功后刷新列表。

### 6. 校验和错误处理

Pydantic 在入口限制长度并拒绝纯空白字符串。资源不存在统一返回清楚的 404；纯空白搜索返回 400；JSON 结构错误保留 FastAPI 的 422。

### 7. API 文档同步

`docs/API.md` 记录路径、方法、载荷、状态码和错误。`/docs-sync` 对照运行中的 `/openapi.json`，只更新文档并列出差异。

### 8. 测试工作流

`/tests` 先快速运行并在首个失败处停止；通过后再统计覆盖率。这样失败信息短，成功时又能看到未覆盖行。

### 9. 重构工作流

`/refactor-module` 先找全部引用，再移动文件、更新调用方，最后检查旧路径并运行 Ruff、Black 和测试。一次完成切换，不留无用兼容层。
