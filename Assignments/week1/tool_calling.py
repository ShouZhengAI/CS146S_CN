import ast
import json
import os
from typing import Any, Dict, List, Optional, Tuple, Callable

from dotenv import load_dotenv
from ollama import chat

load_dotenv()

NUM_RUNS_TIMES = 3


# ==========================
# 工具实现（“执行器”）
# ==========================
def _annotation_to_str(annotation: Optional[ast.AST]) -> str:
    if annotation is None:
        return "None"
    try:
        return ast.unparse(annotation)  # type: ignore[attr-defined]
    except Exception:
        # 尽力回退处理
        if isinstance(annotation, ast.Name):
            return annotation.id
        return type(annotation).__name__


def _list_function_return_types(file_path: str) -> List[Tuple[str, str]]:
    with open(file_path, "r", encoding="utf-8") as f:
        source = f.read()
    tree = ast.parse(source)
    results: List[Tuple[str, str]] = []
    for node in tree.body:
        if isinstance(node, ast.FunctionDef):
            return_str = _annotation_to_str(node.returns)
            results.append((node.name, return_str))
    # 排序以确保输出稳定
    results.sort(key=lambda x: x[0])
    return results


def output_every_func_return_type(file_path: str = None) -> str:
    """工具：为每个顶层函数返回以换行符分隔的“名称: 返回类型”列表。"""
    path = file_path or __file__
    if not os.path.isabs(path):
        # 如果不是绝对路径，则尝试以本脚本所在目录为基准查找文件
        candidate = os.path.join(os.path.dirname(__file__), path)
        if os.path.exists(candidate):
            path = candidate
    pairs = _list_function_return_types(path)
    return "\n".join(f"{name}: {ret}" for name, ret in pairs)


# 示例函数，确保存在可供分析的内容
def add(a: int, b: int) -> int:
    return a + b


def greet(name: str) -> str:
    return f"Hello, {name}!"

# 工具注册表：用于按名称动态执行工具
TOOL_REGISTRY: Dict[str, Callable[..., str]] = {
    "output_every_func_return_type": output_every_func_return_type,
}

# ==========================
# 提示词脚手架
# ==========================

# 约束模型仅生成执行器能够解析的工具调用。
YOUR_SYSTEM_PROMPT = """
你是工具调用助手。用户要求立即调用工具时，只返回一个合法 JSON 对象，不要输出
Markdown 代码围栏、解释或其他文字。唯一可用工具是
output_every_func_return_type，它读取 Python 文件并列出所有顶层函数的返回类型。
必须使用如下格式，并保持字段名完全一致：
{"tool": "output_every_func_return_type", "args": {"file_path": "tool_calling.py"}}
file_path 必须是字符串。当前任务应直接返回上面这个工具调用。
"""


def resolve_path(p: str) -> str:
    if os.path.isabs(p):
        return p
    here = os.path.dirname(__file__)
    c1 = os.path.join(here, p)
    if os.path.exists(c1):
        return c1
    # 如有需要，尝试项目根目录的同级路径
    return p


def extract_tool_call(text: str) -> Dict[str, Any]:
    """从模型输出中解析一个 JSON 对象。"""
    text = text.strip()
    # 某些模型会用代码围栏包裹 JSON；尝试移除围栏
    if text.startswith("```") and text.endswith("```"):
        text = text.strip("`")
        if text.lower().startswith("json\n"):
            text = text[5:]
    try:
        obj = json.loads(text)
        return obj
    except json.JSONDecodeError:
        raise ValueError("模型未返回有效的工具调用 JSON")


def run_model_for_tool_call(system_prompt: str) -> Dict[str, Any]:
    response = chat(
        model="llama3.1:8b",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": "请立即调用工具。"},
        ],
        options={"temperature": 0.3},
    )
    content = response.message.content
    return extract_tool_call(content)


def execute_tool_call(call: Dict[str, Any]) -> str:
    name = call.get("tool")
    if not isinstance(name, str):
        raise ValueError("工具调用 JSON 中缺少字符串字段 'tool'")
    func = TOOL_REGISTRY.get(name)
    if func is None:
        raise ValueError(f"未知工具：{name}")
    args = call.get("args", {})
    if not isinstance(args, dict):
        raise ValueError("工具调用 JSON 中的 'args' 必须是一个对象")

    # 如果存在 file_path 参数，则尽力解析其路径
    if "file_path" in args and isinstance(args["file_path"], str):
        args["file_path"] = resolve_path(args["file_path"]) if str(args["file_path"]) != "" else __file__
    elif "file_path" not in args:
        # 为需要 file_path 的工具提供默认值
        args["file_path"] = __file__

    return func(**args)


def compute_expected_output() -> str:
    # 根据文件的实际内容计算真实的预期输出
    return output_every_func_return_type(__file__)


def test_your_prompt(system_prompt: str) -> bool:
    """运行测试：要求模型生成有效的工具调用，并将工具输出与预期结果比较。"""
    expected = compute_expected_output()
    for _ in range(NUM_RUNS_TIMES):
        try:
            call = run_model_for_tool_call(system_prompt)
        except Exception as exc:
            print(f"解析工具调用失败：{exc}")
            continue
        print(call)
        try:
            actual = execute_tool_call(call)
        except Exception as exc:
            print(f"工具执行失败：{exc}")
            continue
        if actual.strip() == expected.strip():
            print(f"生成的工具调用：{call}")
            print(f"生成的输出：{actual}")
            print("SUCCESS")
            return True
        else:
            print("预期输出：\n" + expected)
            print("实际输出：\n" + actual)
    return False


if __name__ == "__main__":
    test_your_prompt(YOUR_SYSTEM_PROMPT)
