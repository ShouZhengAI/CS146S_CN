# Stack 1：Focus Notes（Bolt 风格 React + FastAPI）

这是同一任务管理应用的 Bolt.new 风格版本。React/Tailwind 提供单页界面，FastAPI 提供 REST API，SQLite 保存任务。支持创建、查看、编辑、完成/取消完成和删除任务。

## 技术栈

- 前端：React、Vite、Tailwind CSS
- 后端：Python、FastAPI、Pydantic
- 数据库：SQLite（首次启动自动生成 `backend/tasks.db`）

## 前置条件

- Node.js 18+
- Python 3.10+

## 启动

后端终端：

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate              # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

前端终端：

```bash
cd frontend
npm install
npm run dev
```

访问 `http://localhost:5173`。API 文档位于 `http://localhost:8000/docs`。

## 环境配置

前端默认请求 `http://localhost:8000/api`。如后端地址不同，在 `frontend/.env` 设置：

```text
VITE_API_URL=http://localhost:8000/api
```

## API

- `GET /api/tasks`、`GET /api/tasks/{id}`
- `POST /api/tasks`
- `PUT /api/tasks/{id}`
- `DELETE /api/tasks/{id}`

请求体为 `{ "title": "...", "notes": "...", "completed": false }`。标题必填且最多 120 字，备注最多 2000 字。

## 生成与手动修复说明

界面按 Bolt.new 常见的渐变/卡片式生成风格设计；导出后手动接入 FastAPI、SQLite、CORS、输入校验和完整错误状态。当前无已知功能偏离；本地开发需同时运行两个进程。
