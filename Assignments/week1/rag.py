import os
import re
from typing import List, Callable
from dotenv import load_dotenv
from ollama import chat

load_dotenv()

NUM_RUNS_TIMES = 5

DATA_FILES: List[str] = [
    os.path.join(os.path.dirname(__file__), "data", "api_docs.txt"),
]


def load_corpus_from_files(paths: List[str]) -> List[str]:
    corpus: List[str] = []
    for p in paths:
        if os.path.exists(p):
            try:
                with open(p, "r", encoding="utf-8") as f:
                    corpus.append(f.read())
            except Exception as exc:
                corpus.append(f"[load_error] {p}: {exc}")
        else:
            corpus.append(f"[missing_file] {p}")
    return corpus


# 从外部文件（简单的 API 文档）加载语料库；如果文件缺失，则回退到内联片段
CORPUS: List[str] = load_corpus_from_files(DATA_FILES)

QUESTION = (
    "编写一个 Python 函数 `fetch_user_name(user_id: str, api_key: str) -> str`，调用文档中说明的 API "
    "按 ID 获取用户，并仅以字符串形式返回该用户的姓名。"
)


# 要求模型把检索到的文档视为唯一事实来源，避免臆造 API。
YOUR_SYSTEM_PROMPT = """
你是一个基于检索文档编写代码的助手。严格遵守用户提供的 API 文档，只使用文档明确
给出的基础 URL、端点、HTTP 方法、认证请求头和响应字段，不得猜测或替换任何值。
完整满足任务中的错误处理与返回值要求。只输出一个带 ```python 围栏的代码块，
代码块中包含必要导入和所要求的函数，不输出解释。
"""


# 对于这个简单示例
# 对于此编程任务，按必需的代码片段进行验证，而不是要求字符串完全一致
REQUIRED_SNIPPETS = [
    "def fetch_user_name(",
    "requests.get",
    "/users/",
    "X-API-Key",
    "return",
]


def YOUR_CONTEXT_PROVIDER(corpus: List[str]) -> List[str]:
    """返回包含当前问题所需 API 信息的文档片段。"""
    query = QUESTION.casefold()
    query_terms = {
        term
        for term in re.findall(r"[a-z][a-z0-9_-]+", query)
        if len(term) > 2
    }
    # 中英文文档可能使用不同说法；这些词覆盖用户、认证和端点信息。
    api_terms = query_terms | {
        "user",
        "users",
        "userclient",
        "api",
        "auth",
        "authentication",
        "endpoint",
        "用户",
        "身份验证",
        "端点",
        "密钥",
    }

    relevant_docs: List[str] = []
    for doc in corpus:
        normalized = doc.casefold()
        if normalized.startswith(("[load_error]", "[missing_file]")):
            continue
        if any(term in normalized for term in api_terms):
            relevant_docs.append(doc)
    return relevant_docs


def make_user_prompt(question: str, context_docs: List[str]) -> str:
    if context_docs:
        context_block = "\n".join(f"- {d}" for d in context_docs)
    else:
        context_block = "（未提供上下文）"
    return (
        f"上下文（只能使用以下信息）：\n{context_block}\n\n"
        f"任务：{question}\n\n"
        "要求：\n"
        "- 使用文档中说明的基础 URL 和端点。\n"
        "- 发送文档中说明的身份验证请求头。\n"
        "- 对非 200 响应调用 raise_for_status()。\n"
        "- 仅返回用户姓名字符串。\n\n"
        "输出：只输出一个带围栏的 Python 代码块，其中包含该函数及必要的导入。\n"
    )


def extract_code_block(text: str) -> str:
    """提取最后一个带围栏的 Python 代码块；若没有，则提取任意带围栏的代码块，否则返回原文本。"""
    # 首先尝试匹配 ```python ... ```
    m = re.findall(r"```python\n([\s\S]*?)```", text, flags=re.IGNORECASE)
    if m:
        return m[-1].strip()
    # 回退为匹配任意带围栏的代码块
    m = re.findall(r"```\n([\s\S]*?)```", text)
    if m:
        return m[-1].strip()
    return text.strip()


def test_your_prompt(system_prompt: str, context_provider: Callable[[List[str]], List[str]]) -> bool:
    """最多运行 NUM_RUNS_TIMES 次；若任意一次输出包含所有 REQUIRED_SNIPPETS，则返回 True。"""
    context_docs = context_provider(CORPUS)
    user_prompt = make_user_prompt(QUESTION, context_docs)

    for idx in range(NUM_RUNS_TIMES):
        print(f"正在运行第 {idx + 1}/{NUM_RUNS_TIMES} 次测试")
        response = chat(
            model="llama3.1:8b",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            options={"temperature": 0.0},
        )
        output_text = response.message.content
        code = extract_code_block(output_text)
        missing = [s for s in REQUIRED_SNIPPETS if s not in code]
        if not missing:
            print(output_text)
            print("SUCCESS")
            return True
        else:
            print("缺少必需的代码片段：")
            for s in missing:
                print(f"  - {s}")
            print("生成的代码：\n" + code)
    return False


if __name__ == "__main__":
    test_your_prompt(YOUR_SYSTEM_PROMPT, YOUR_CONTEXT_PROVIDER)
