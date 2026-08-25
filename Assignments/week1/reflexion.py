import os
import re
from typing import Callable, List, Tuple
from dotenv import load_dotenv
from ollama import chat

load_dotenv()

NUM_RUNS_TIMES = 1

SYSTEM_PROMPT = """
你是一名编程助手。只输出一个带围栏的 Python 代码块，其中定义函数
is_valid_password(password: str) -> bool。不要输出说明文字或注释。
实现应尽可能精简。
"""

# 要求模型依据真实失败样例定位缺失规则，而不是重新猜测需求。
YOUR_REFLEXION_PROMPT = """
你是一名负责修复代码的编程助手。用户会提供上一版实现和未通过的测试反馈。
逐条分析“预期、实际、未通过的检查”，修正根因，并保留已经正确的行为。
is_valid_password 的完整规则是：长度至少 8；至少包含一个小写字母、一个大写字母、
一个数字和一个属于 !@#$%^&*()-_ 的特殊字符；不能包含空白字符。
返回完整的替代实现。只输出一个带围栏的 Python 代码块，其中定义
is_valid_password(password: str) -> bool；不要输出解释、注释或测试代码。
"""


# 用于评估生成代码的真实测试套件
SPECIALS = set("!@#$%^&*()-_")
TEST_CASES: List[Tuple[str, bool]] = [
    ("Password1!", True),       # 有效
    ("password1!", False),      # 缺少大写字母
    ("Password!", False),       # 缺少数字
    ("Password1", False),       # 缺少特殊字符
]


def extract_code_block(text: str) -> str:
    m = re.findall(r"```python\n([\s\S]*?)```", text, flags=re.IGNORECASE)
    if m:
        return m[-1].strip()
    m = re.findall(r"```\n([\s\S]*?)```", text)
    if m:
        return m[-1].strip()
    return text.strip()


def load_function_from_code(code_str: str) -> Callable[[str], bool]:
    namespace: dict = {}
    exec(code_str, namespace)  # noqa: S102（本练习会执行由模型生成的受控代码）
    func = namespace.get("is_valid_password")
    if not callable(func):
        raise ValueError("生成的代码中未找到可调用的 is_valid_password")
    return func


def evaluate_function(func: Callable[[str], bool]) -> Tuple[bool, List[str]]:
    failures: List[str] = []
    for pw, expected in TEST_CASES:
        try:
            result = bool(func(pw))
        except Exception as exc:
            failures.append(f"输入：{pw} → 引发异常：{exc}")
            continue

        if result != expected:
            # 根据真实规则计算诊断信息
            reasons = []
            if len(pw) < 8:
                reasons.append("长度小于 8")
            if not any(c.islower() for c in pw):
                reasons.append("缺少小写字母")
            if not any(c.isupper() for c in pw):
                reasons.append("缺少大写字母")
            if not any(c.isdigit() for c in pw):
                reasons.append("缺少数字")
            if not any(c in SPECIALS for c in pw):
                reasons.append("缺少特殊字符")
            if any(c.isspace() for c in pw):
                reasons.append("包含空白字符")

            failures.append(
                f"输入：{pw} → 预期为 {expected}，实际为 {result}。未通过的检查：{', '.join(reasons) or '未知'}"
            )

    return (len(failures) == 0, failures)


def generate_initial_function(system_prompt: str) -> str:
    response = chat(
        model="llama3.1:8b",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": "请立即提供实现。"},
        ],
        options={"temperature": 0.2},
    )
    return extract_code_block(response.message.content)


def your_build_reflexion_context(prev_code: str, failures: List[str]) -> str:
    """把上一版代码和逐条失败反馈整理成可直接修复的上下文。"""
    failure_text = "\n".join(f"{index}. {failure}" for index, failure in enumerate(failures, 1))
    if not failure_text:
        failure_text = "没有记录到失败信息；请按完整规则复核实现。"
    return (
        "请根据测试反馈修复下面的实现，并输出完整替代代码。\n\n"
        "上一版实现：\n"
        f"```python\n{prev_code.strip()}\n```\n\n"
        "未通过的测试：\n"
        f"{failure_text}\n\n"
        "修复要求：覆盖所有失败的根因，同时保持已通过用例的行为不变。"
    )


def apply_reflexion(
    reflexion_prompt: str,
    build_context: Callable[[str, List[str]], str],
    prev_code: str,
    failures: List[str],
) -> str:
    reflection_context = build_context(prev_code, failures)
    print(f"反思上下文：{reflection_context}，{reflexion_prompt}")
    response = chat(
        model="llama3.1:8b",
        messages=[
            {"role": "system", "content": reflexion_prompt},
            {"role": "user", "content": reflection_context},
        ],
        options={"temperature": 0.2},
    )
    return extract_code_block(response.message.content)


def run_reflexion_flow(
    system_prompt: str,
    reflexion_prompt: str,
    build_context: Callable[[str, List[str]], str],
) -> bool:
    # 1）生成初始函数
    initial_code = generate_initial_function(system_prompt)
    print("初始代码：\n" + initial_code)
    func = load_function_from_code(initial_code)
    passed, failures = evaluate_function(func)
    if passed:
        print("SUCCESS（初始实现通过了所有测试）")
        return True
    else:
        print(f"FAILURE（初始实现未通过部分测试）：{failures}")

    # 2）进行一轮反思
    improved_code = apply_reflexion(reflexion_prompt, build_context, initial_code, failures)
    print("\n改进后的代码：\n" + improved_code)
    improved_func = load_function_from_code(improved_code)
    passed2, failures2 = evaluate_function(improved_func)
    if passed2:
        print("SUCCESS")
        return True

    print("反思后仍未通过的测试：")
    for f in failures2:
        print("- " + f)
    return False


if __name__ == "__main__":
    run_reflexion_flow(SYSTEM_PROMPT, YOUR_REFLEXION_PROMPT, your_build_reflexion_context)
