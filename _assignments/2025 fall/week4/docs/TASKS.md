# 仓库任务清单

## 1) 启用 pre-commit 并修复仓库问题
- 安装钩子：`pre-commit install`
- 运行：`pre-commit run --all-files`
- 修复所有格式化/代码检查问题（black/ruff）

## 2) 为笔记添加搜索端点
- 使用 SQLAlchemy 过滤器添加/扩展 `GET /notes/search?q=...`（不区分大小写）
- 更新 `frontend/app.js` 以使用搜索查询
- 在 `backend/tests/test_notes.py` 中添加测试

## 3) 完善行动项流程
- 实现 `PUT /action-items/{id}/complete`（已有脚手架）
- 更新界面以反映完成状态（相关逻辑已接入），并扩充测试覆盖范围

## 4) 改进提取逻辑
- 扩展 `backend/app/services/extract.py`，使其能够解析 `#tag` 之类的标签并返回这些标签
- 为新的解析行为添加测试
- （可选）提供 `POST /notes/{id}/extract`，用于将笔记转换为行动项

## 5) 增强笔记的 CRUD 功能
- 添加 `PUT /notes/{id}` 以编辑笔记（标题/内容）
- 添加 `DELETE /notes/{id}` 以删除笔记
- 更新 `frontend/app.js` 以支持编辑/删除，并添加测试

## 6) 请求验证与错误处理
- 在 `schemas.py` 中添加简单的验证规则（例如最小长度）
- 在适当情况下返回信息明确的 400/404 错误，并为验证失败场景添加测试

## 7) 文档偏差检查（目前手动执行）
- 创建/维护一份简明的 `API.md`，用于说明端点和请求/响应载荷
- 每次更改后，验证文档是否与实际 OpenAPI（`/openapi.json`）一致
