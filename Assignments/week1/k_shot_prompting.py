import os
from dotenv import load_dotenv
from ollama import chat

load_dotenv()

NUM_RUNS_TIMES = 5

# 用多个示例明确演示“逐词反转”，并固定输出格式。
YOUR_SYSTEM_PROMPT = """
你是一个严格的字符串转换器。把输入中每个待处理单词的字母从右到左排列。
保持字符的大小写和内容不变；只改变顺序。只输出转换后的结果，不要解释、不要加引号或标点。

示例：
输入：cat
输出：tac

输入：hello
输出：olleh

输入：prompt
输出：tpmorp

输入：OpenAI
输出：IAnepO
"""

USER_PROMPT = """
将下列单词中的字母顺序反转。只输出反转后的单词，不要输出任何其他文本：

httpstatus
"""


EXPECTED_OUTPUT = "sutatsptth"

def test_your_prompt(system_prompt: str) -> bool:
    """最多运行 NUM_RUNS_TIMES 次提示；若任意一次输出与 EXPECTED_OUTPUT 匹配，则返回 True。

    找到匹配项时打印“SUCCESS”。
    """
    for idx in range(NUM_RUNS_TIMES):
        print(f"正在运行第 {idx + 1}/{NUM_RUNS_TIMES} 次测试")
        response = chat(
            model="mistral-nemo:12b",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": USER_PROMPT},
            ],
            options={"temperature": 0.5},
        )
        output_text = response.message.content.strip()
        if output_text.strip() == EXPECTED_OUTPUT.strip():
            print("SUCCESS")
            return True
        else:
            print(f"预期输出：{EXPECTED_OUTPUT}")
            print(f"实际输出：{output_text}")
    return False

if __name__ == "__main__":
    test_your_prompt(YOUR_SYSTEM_PROMPT)