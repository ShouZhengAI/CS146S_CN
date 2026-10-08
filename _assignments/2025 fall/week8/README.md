# 第 8 周：三种技术栈实现同一任务应用

本周用三套独立技术栈实现 **Focus Tasks**。三个版本的数据模型和功能一致：任务包含标题、备注、完成状态与时间戳；用户可以创建、查看、编辑、切换状态和删除，数据都保存在 SQLite。

## 项目一览

| 版本 | 前端 | 后端 | 持久化 | 特点 |
|---|---|---|---|---|
| [`stack1-bolt-react`](./stack1-bolt-react/) | React + Vite + Tailwind | FastAPI | SQLite | Bolt.new 风格，前后端分离，交互丰富 |
| [`stack2-django`](./stack2-django/) | Django Templates | Django | Django ORM + SQLite | 完整全栈、表单、Admin、JSON API |
| [`stack3-flask-sqlite`](./stack3-flask-sqlite/) | 原生 HTML/CSS/JS | Flask | SQLite | 依赖少，Fetch 单页交互，结构直观 |

每个目录都有独立依赖和运行说明，项目之间不共享运行时或数据库。

## 统一功能

- 创建带标题和备注的任务
- 查看持久化任务列表
- 编辑标题、备注和完成状态
- 一键完成或恢复任务
- 删除前确认
- 前后端输入校验、空状态和错误提示
- REST 风格接口（Django 同时提供服务端页面 CRUD）

## 架构

### Stack 1

```text
React/Tailwind → Fetch → FastAPI/Pydantic → sqlite3 → tasks.db
```

浏览器和 API 分开运行。前端负责交互状态，FastAPI 负责校验、错误码与数据库操作。

### Stack 2

```text
浏览器 → Django URL/View → ModelForm/Template → ORM → db.sqlite3
                         └→ JSON API
```

Django 在同一项目内管理模型、页面、表单、路由、Admin 和 API，服务端渲染页面无需前端构建。

### Stack 3

```text
HTML/CSS/Vanilla JS → Fetch → Flask → sqlite3 → tasks.db
```

Flask 提供页面和 API；原生 JavaScript 集中维护列表状态并安全更新 DOM。

## 三种方案比较

- **开发速度：** Django 内置 ORM、表单、迁移和后台，标准 CRUD 最省样板代码。
- **前端体验：** React 的组件状态适合复杂交互，但要单独管理前后端依赖与 CORS。
- **简单程度：** Flask + 原生 JS 文件少、链路清楚；功能变大后需要更主动地组织状态和模块。
- **数据访问：** Django ORM 可读性最好；FastAPI/Flask 直接使用参数化 SQL，更容易看清实际查询。
- **部署方式：** Django、Flask 可单进程提供页面；React + FastAPI 通常分别构建和部署。

## 解题思路

1. 先固定统一数据模型和 CRUD 验收流程，保证三个版本功能可比较。
2. 每套技术栈独立建目录、依赖和数据库，避免配置互相影响。
3. 先完成持久化与 API，再连接界面；所有写操作都由服务端校验。
4. 更新和删除先检查资源是否存在，失败返回明确的 4xx 错误。
5. 界面覆盖加载、空列表、编辑、删除确认和错误状态，不只做静态页面。
6. README 写清前置条件、安装、启动、环境配置和已知限制，保证别人能独立运行。

具体启动命令见三个项目各自的 `README.md`。
