# 第 2 周：行动项提取器

## 项目简介

这是一个 FastAPI + SQLite 小应用，用来把会议记录或自由文本转换成行动项。它提供两种提取方式：

- 规则提取：识别项目符号、复选框、`TODO:`、`Action:`、`Next:` 等格式，速度快且无需模型。
- LLM 提取：调用本机 Ollama，按 JSON Schema 返回结构化行动项；模型不可用或返回格式错误时自动回退到规则提取。

网页端可以输入笔记、选择是否保存、提取行动项、勾选完成状态，也可以列出已保存笔记。数据保存在 `week2/data/app.db`，首次启动时自动创建。

## 环境配置

要求：Python 3.10+、Poetry；使用 LLM 功能时还需要 Ollama。

```bash
# 在仓库根目录安装依赖
poetry install

# 安装 Ollama 后拉取默认模型
ollama pull llama3.2:3b
```

默认模型是 `llama3.2:3b`。如需更换模型，在启动服务前设置环境变量：

```bash
export OLLAMA_MODEL=gemma3:4b
```

Ollama 桌面程序通常会自动启动服务；命令行环境可另行运行 `ollama serve`。

## 启动与使用

在仓库根目录运行：

```bash
poetry run uvicorn week2.app.main:app --reload
```

打开 <http://127.0.0.1:8000/>。输入笔记后：

1. “Extract”使用本地规则提取。
2. “使用 LLM 提取”调用 Ollama；首次推理可能较慢。
3. 勾选“Save as note”会同时保存原始笔记。
4. “列出笔记”显示数据库中的全部笔记，最新记录排在前面。

FastAPI 自动接口文档位于 <http://127.0.0.1:8000/docs>。

## API 端点

| 方法 | 路径 | 功能 | 请求体/参数 |
| --- | --- | --- | --- |
| `GET` | `/` | 返回网页界面 | 无 |
| `POST` | `/notes` | 新建笔记 | `{"content": "..."}` |
| `GET` | `/notes` | 列出全部笔记，按 ID 倒序 | 无 |
| `GET` | `/notes/{note_id}` | 获取单条笔记 | 路径参数 `note_id` |
| `POST` | `/notes/extract-llm` | 用 Ollama 提取行动项，可保存原笔记 | `{"text": "...", "save_note": true}` |
| `POST` | `/action-items/extract` | 用规则提取行动项，可保存原笔记 | `{"text": "...", "save_note": true}` |
| `GET` | `/action-items` | 列出行动项；可按笔记过滤 | 可选查询参数 `note_id` |
| `POST` | `/action-items/{id}/done` | 修改完成状态 | `{"done": true}` |

两个提取端点都返回：

```json
{
  "note_id": 1,
  "items": [{"id": 1, "text": "Write tests"}]
}
```

未保存笔记时 `note_id` 为 `null`。缺少必填文本时返回 HTTP 400。LLM 调用失败不会让请求崩溃，而是使用本地规则继续提取。

## 测试

在仓库根目录运行第 2 周测试：

```bash
poetry run pytest week2/tests -v
```

只运行提取服务测试：

```bash
poetry run pytest week2/tests/test_extract.py -v
```

测试通过 mock 替代真实 Ollama 调用，因此不要求下载模型，也不依赖网络。覆盖项目符号、关键字前缀、空输入、无结构文本、结构化模型响应、重复项和旧模型可能返回的 JSON 代码块。

## 目录结构

```text
week2/
├── app/
│   ├── main.py                 # FastAPI 应用入口
│   ├── db.py                   # SQLite 读写
│   ├── routers/                # 笔记与行动项接口
│   └── services/extract.py     # 规则与 LLM 提取逻辑
├── frontend/index.html         # 无构建步骤的网页端
├── tests/test_extract.py       # 提取逻辑单元测试
└── writeup.md                  # 作业过程记录
```

## 各练习的解题思路

### 练习 1：LLM 提取

给 Ollama 明确的系统提示，并用 JSON Schema 限定返回值为字符串数组。解析时兼容对象响应、字典响应和 Markdown JSON 代码块；清理空项并按大小写去重。模型不可用或 JSON 异常时调用原有规则函数，保证基本功能可用。

### 练习 2：单元测试

所有模型调用都 mock 掉，测试只验证自己的输入、解析和回退逻辑。分别覆盖项目符号、关键字、空白输入、普通叙述和规范 JSON 响应，避免测试受网络和模型随机性影响。

### 练习 3：代码清理

把“读取响应”和“解析行动项”拆成小函数，让每个函数只做一件事。路由统一检查空文本并返回固定结构；数据库操作继续集中在 `db.py`，前端不依赖 SQLite 细节。

### 练习 4：接口与网页集成

新增 `/notes/extract-llm` 和 `GET /notes`。前端两个按钮分别调用接口，并用 DOM API写入模型文本和笔记内容，避免把用户内容直接拼进 HTML；请求失败时显示后端错误并恢复按钮状态。

### 练习 5：README

先按入口文件、路由、服务、数据库和测试梳理实际行为，再记录可直接执行的安装、启动和测试命令。接口表写清方法、路径、输入和作用，便于第一次接触项目的人快速运行与排错。
