# 第 8 周作业报告

## 提交信息

姓名：**未提供（提交前填写）**  
SUNet ID：**未提供（提交前填写）**  
引用资料：**Django、FastAPI、Flask、React、Vite 与 Tailwind CSS 官方文档；Bolt.new 产品说明**

我大约花了 **12** 小时完成这项作业。

## 应用概念

**Focus Tasks** 是一个个人任务与备注管理器。用户可以创建任务、查看列表、修改标题和备注、切换完成状态、删除任务；三个版本都把数据持久化到 SQLite，并提供输入校验、错误提示和完整 CRUD 流程。相同需求分别用前后端分离、Django 全栈、Flask 加原生 JavaScript 实现，便于直接比较开发体验。

## 版本 1 说明

### 应用详情

- 文件夹名称：`stack1-bolt-react`
- AI 应用生成平台：Bolt.new（用于界面方向、组件结构和初始提示迭代）
- 技术栈：React + Vite + Tailwind CSS 前端，FastAPI 后端
- 持久化方案：Python 标准库 `sqlite3`，数据库文件为 `backend/tasks.db`
- 使用的框架/库：React、Vite、Tailwind CSS、FastAPI、Pydantic、Uvicorn
- 核心流程截图：未附截图；运行后首页可完成新建、编辑、状态切换和删除

### 反思

**a. 问题及解决方法：** Bolt 风格前端最初只有浏览器内状态，刷新后数据丢失。我将数据操作统一改为调用 FastAPI REST 接口，并在后端用参数化 SQL 接入 SQLite。前后端端口不同导致跨域限制，因此只为本地 Vite 地址配置 CORS。错误响应在前端统一解析并显示，空标题则前后端同时拦截。

**b. 提示词设计：** 首次提示明确“单页任务管理器、深色现代卡片、标题/备注/完成状态、移动端适配”，能快速得到稳定布局。后续提示一次只解决一个问题：先列出数据模型和五个 CRUD 接口，再要求加载/空/错误状态，最后要求可访问性和删除确认。“做一个漂亮的任务应用”过于宽泛，容易只生成静态界面；明确字段、端点和验收流程效果更好。

示例提示词：

> Build a responsive task-and-notes dashboard with React, Vite and Tailwind. A task has id, title, notes, completed and timestamps. Provide create, list, edit, toggle and delete flows, including loading, empty and error states. Connect every action to a FastAPI REST API backed by SQLite; do not use mock data or localStorage.

**c. 用时：** 从开始到前端首次运行约 25 分钟；到 FastAPI、SQLite 和完整 CRUD 可用约 4 小时。

## 版本 2 说明

### 应用详情

- 文件夹名称：`stack2-django`
- AI 应用生成平台：未使用生成平台；按 Django 官方项目结构实现
- 技术栈：Python Django 服务端全栈、Django Templates、HTML/CSS
- 持久化方案：Django ORM + SQLite，数据库文件为 `db.sqlite3`
- 使用的框架/库：Django Model、ModelForm、Templates、Admin、JsonResponse
- 核心流程截图：未附截图；首页列表包含新建、编辑、完成切换和删除入口

### 反思

**a. 问题及解决方法：** Django 的页面 CRUD 与 JSON API 有不同输入形式。页面使用 `ModelForm` 复用模型约束和 CSRF 防护，API 单独解析 JSON 并返回一致的 4xx 错误。删除操作使用确认页和 POST，避免 GET 产生副作用。提交初始迁移文件，让新环境只需执行 `migrate` 即可运行；Admin 注册后可搜索和筛选任务。

**b. 提示词设计：** 最有效的提示是指定 Django 的每一层：`Task` 模型字段、ModelForm、函数视图、命名路由、模板、Admin 和迁移。额外强调“服务端渲染 CRUD 必须无需 JavaScript”和“不安全页面操作使用 POST + CSRF”，可以避免只有 API 或不安全删除链接。要求同时添加 JSON API时，需要明确返回字段、方法和状态码。

示例提示词：

> Create a Django task board using one Task model and SQLite. Implement server-rendered list/create/update/toggle/delete pages with ModelForm, CSRF and a delete confirmation. Register the model in Admin, commit the initial migration, and expose GET/POST plus GET/PUT/DELETE JSON endpoints with validation. Do not depend on a separate frontend.

**c. 用时：** 从项目结构开始到首页首次运行约 35 分钟；到模板、Admin、迁移与双套 CRUD 完成约 3.5 小时。

## 版本 3 说明

### 应用详情

- 文件夹名称：`stack3-flask-sqlite`
- AI 应用生成平台：未使用生成平台；以轻量、少依赖为目标手动实现
- 技术栈：Python Flask + 原生 JavaScript/HTML5/CSS
- 持久化方案：Python `sqlite3`，数据库文件为 `tasks.db`
- 使用的框架/库：Flask、Jinja2、Fetch API、原生 DOM API
- 核心流程截图：未附截图；单页界面可进行 CRUD、状态切换和筛选

### 反思

**a. 问题及解决方法：** 原生 JavaScript 没有组件状态管理，需要避免 DOM 与数据库状态不同步。我将服务器结果保存在一个任务数组中，每次写操作成功后重新加载并集中渲染。所有用户文本用 `textContent` 写入，避免把备注当 HTML 注入；SQL 使用占位符。Flask 应用启动时自动建表，应用上下文结束时关闭连接，错误统一返回 JSON。

**b. 提示词设计：** 提示词强调“不使用前端框架、不使用 localStorage、只用 Fetch 与 DOM API”，可以防止生成多余依赖。把交互拆成表单状态、任务渲染、筛选、编辑回填、删除确认和错误区域后，生成结果更容易检查。需要额外明确移动端布局、键盘焦点样式和 `aria` 标签，否则生成器常只关注视觉效果。

示例提示词：

> Build a clean mobile-friendly Flask task manager using one HTML5 page, vanilla CSS and vanilla JavaScript only. Use Fetch against SQLite-backed REST endpoints for full CRUD. Include inline editing, completion toggle, all/open/done filtering, empty and error states, delete confirmation, accessible labels, server validation and parameterized SQL. Do not use localStorage or frontend packages.

**c. 用时：** 从 Flask 页面首次运行约 20 分钟；到 REST API、SQLite、筛选和完整交互完成约 3 小时。
