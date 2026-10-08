# Stack 3：Clearlist（Flask + Vanilla JS + SQLite）

轻量任务管理器：Flask 同时提供静态页面与 REST API，原生 JavaScript 无刷新更新界面，SQLite 持久化任务。支持新增、读取、编辑、完成/取消完成、筛选和删除。

## 前置条件

- Python 3.10+

## 安装与运行

```bash
python3 -m venv .venv
source .venv/bin/activate              # Windows: .venv\Scripts\activate
pip install -r requirements.txt
flask --app app run --debug
```

访问 `http://127.0.0.1:5000/`。首次启动自动创建 `tasks.db`，无需手动建表。

## 配置与数据

默认仅需本地 SQLite 文件，无环境变量。生产部署时应关闭调试模式，并使用 Gunicorn/Waitress 等 WSGI 服务器。备份或重置数据时处理项目根目录的 `tasks.db`（重置可在停止服务后删除该文件）。

## REST API

- `GET /api/tasks`、`GET /api/tasks/{id}`
- `POST /api/tasks`
- `PUT /api/tasks/{id}`
- `DELETE /api/tasks/{id}`

写请求使用 JSON：`{ "title": "...", "notes": "...", "completed": false }`。服务端校验空标题和字段长度，并对格式错误、资源不存在返回明确的 4xx JSON。

## 偏离、手动修复与已知问题

没有偏离最低功能范围。手动加入筛选、空状态、错误提示、删除确认、无障碍标签以及服务端参数化 SQL。为保持轻量，未加入登录和多用户隔离；该版本定位为单机个人任务清单。
