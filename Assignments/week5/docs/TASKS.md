# 代码仓库任务

## 1) 将前端迁移至 Vite + React（复杂）
- 在 `week5/frontend/` 中搭建 Vite + React 应用（也可放在类似 `week5/frontend/ui/` 的子目录中）。
- 使用由 FastAPI 提供服务的构建产物替换当前静态资源：
  - 构建到 `week5/frontend/dist/`。
  - 更新 FastAPI 的静态目录挂载，使其提供 `dist` 中的内容，并让根路径（`/`）返回 `dist` 中的 `index.html`。
- 在 React 中接入现有端点：
  - 笔记的列表、创建、删除和编辑。
  - 待办事项的列表、创建和完成。
- 更新 `Makefile`，加入 `web-install`、`web-dev`、`web-build` 目标，并确保 `make run` 自动构建 Web 产物（或在文档中说明该工作流）。
- 为至少两个组件添加组件/单元测试（React Testing Library），并在 `backend/tests` 中添加 API 兼容性集成测试。

## 2) 支持分页和排序的笔记搜索（中等）
- 实现 `GET /notes/search?q=...&page=1&page_size=10&sort=created_desc|title_asc`。
- 对标题/内容使用不区分大小写的匹配。
- 返回包含 `items`、`total`、`page`、`page_size` 的响应数据。
- 使用 SQLAlchemy 组合查询，实现筛选、排序和分页。
- 更新 React 界面，加入搜索输入框、结果数量以及上一页/下一页分页控件。
- 在 `backend/tests/test_notes.py` 中添加针对查询边界情况和分页的测试。

## 3) 完整的笔记 CRUD 与乐观式界面更新（中等）
- 添加 `PUT /notes/{id}` 和 `DELETE /notes/{id}`。
- 在前端进行乐观式状态更新，并在发生错误时执行回滚。
- 在 `schemas.py` 中验证请求数据（最小长度，以及适当的最大长度）。
- 添加成功场景和验证错误场景的测试。

## 4) 待办事项：筛选与批量完成（中等）
- 添加 `GET /action-items?completed=true|false`，按完成状态进行筛选。
- 添加 `POST /action-items/bulk-complete`，接收 ID 列表并在一个事务中将对应事项标记为已完成。
- 更新前端，加入筛选开关和批量操作界面。
- 添加测试，覆盖筛选、批量操作行为，以及出错时的事务回滚。

## 5) 具有多对多关系的标签功能（复杂）
- 添加 `Tag` 模型和连接表 `note_tags`（`Note` 与 `Tag` 之间为多对多关系）。
- 端点：
  - `GET /tags`、`POST /tags`、`DELETE /tags/{id}`
  - 使用 `POST /notes/{id}/tags` 关联标签，使用 `DELETE /notes/{id}/tags/{tag_id}` 解除关联
- 更新提取功能（参见下一个任务），根据 `#hashtags` 自动创建并关联标签。
- 更新界面，以标签块形式显示标签，并支持按标签筛选笔记。
- 添加针对模型关系和端点行为的测试。

## 6) 改进提取逻辑和端点（中等）
- 扩展 `backend/app/services/extract.py`，使其能够解析：
  - `#hashtags` → 标签
  - `- [ ] task text` → 待办事项
- 添加 `POST /notes/{id}/extract`：
  - 返回结构化提取结果；当 `apply=true` 时，还可选择持久化新标签/待办事项。
- 添加针对提取解析和 `apply=true` 持久化路径的测试。

## 7) 健壮的错误处理和响应封装（简单至中等）
- 使用 Pydantic 模型添加验证（最小长度约束、非空字符串）。
- 添加全局异常处理器，返回统一的 JSON 封装：
  - `{ "ok": false, "error": { "code": "NOT_FOUND", "message": "..." } }`
  - 成功响应：`{ "ok": true, "data": ... }`
- 更新测试，断言成功和错误场景下的响应封装结构。

## 8) 为所有集合的列表端点添加分页（简单）
- 为 `GET /notes` 和 `GET /action-items` 添加 `page` 和 `page_size`。
- 分别返回 `items` 和 `total`。
- 更新前端，为列表加入分页；添加边界测试（最后一页为空、页面大小过大）。

## 9) 查询性能与索引（简单至中等）
- 在有益的位置添加 SQLite 索引（例如 `notes.title`、标签连接表）。
- 通过植入较大数据集的测试验证查询计划有所改进，并确保没有性能回退。

## 10) 改进测试覆盖率（简单）
- 添加测试以覆盖：
  - 每个端点的 400/404 场景
  - 批量操作的并发/事务行为
  - 搜索、分页和乐观式更新的前端集成测试（可以使用模拟或轻量级方案）

## 11) 可部署至 Vercel（中等至复杂）
- 使用 Vite + React 的前端：
  - 添加包含 `build` 和 `preview` 脚本的 `package.json`，并配置 Vite 将输出写入 `frontend/dist`（或 `frontend/ui/dist`）。
  - 添加 `vercel.json`，将项目根目录设置为 `week5/frontend`，并将 `outputDirectory` 设置为 `dist`。
  - 在构建时注入 `VITE_API_BASE_URL`，使其指向 API。
- Vercel 上的 API（方案 A：无服务器 FastAPI）：
  - 创建 `week5/api/index.py`，从 `backend/app/main.py` 导入 FastAPI 的 `app`。
  - 确保 Vercel 能够获取 Python 依赖项（为函数使用 `pyproject.toml` 或 `requirements.txt`）。
  - 配置 CORS，允许 Vercel 前端源站访问。
  - 更新 `vercel.json`，将 `/api/*` 路由到 Python 函数，并为其他路由提供 React 应用。
- 部署在其他位置的 API（方案 B）：
  - 将后端部署到 Fly.io 或 Render 等服务。
  - 配置 Vercel 前端，使其通过 `VITE_API_BASE_URL` 调用外部 API，并设置任何必要的重写/代理。
- 在 `README.md` 中添加简短的部署指南，其中包括环境变量、构建命令和回滚方法。
