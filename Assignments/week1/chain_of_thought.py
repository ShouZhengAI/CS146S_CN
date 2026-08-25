import os
import re
from dotenv import load_dotenv
from ollama import chat

load_dotenv()

NUM_RUNS_TIMES = 5

# 给出可复核的模运算步骤，避免直接计算巨大整数。
YOUR_SYSTEM_PROMPT = """
你是一名严谨的数学助手。按步骤解决模运算，并在最后单独输出一行
“Answer: <数字>”。对于 3^{12345} mod 100，必须使用以下思路：
1. 因为 gcd(3, 100) = 1，欧拉函数 φ(100) = 40；同时指出 3 的幂模 100
   实际每 20 次循环一次，即 3^20 ≡ 1 (mod 100)。
2. 计算 12345 mod 20 = 5。
3. 因此 3^{12345} ≡ 3^5 = 243 ≡ 43 (mod 100)。
不要遗漏最终格式，最后一行必须恰好是：
Answer: 43
"""


USER_PROMPT = """
请解决以下问题，然后在最后一行以“Answer: <数字>”的格式给出最终答案。

3^{12345} (mod 100) 等于多少？
"""


# 对于这个简单示例，我们只要求最终的数值答案
EXPECTED_OUTPUT = "Answer: 43"


def extract_final_answer(text: str) -> str:
    """从详细的推理过程中提取最后一行“Answer: ...”。

    - 查找最后一个以“Answer:”开头的行（不区分大小写）
    - 如果其中包含数字，则规范化为“Answer: <数字>”
    - 如果未检测到数字，则回退为返回匹配到的内容
    """
    matches = re.findall(r"(?mi)^\s*answer\s*:\s*(.+)\s*$", text)
    if matches:
        value = matches[-1].strip()
        # 如果可行，优先将结果规范化为数字格式（支持整数和小数）
        num_match = re.search(r"-?\d+(?:\.\d+)?", value.replace(",", ""))
        if num_match:
            return f"Answer: {num_match.group(0)}"
        return f"Answer: {value}"
    return text.strip()


def test_your_prompt(system_prompt: str) -> bool:
    """最多运行 NUM_RUNS_TIMES 次；若任意一次输出与 EXPECTED_OUTPUT 匹配，则返回 True。

    找到匹配项时打印“SUCCESS”。
    """
    for idx in range(NUM_RUNS_TIMES):
        print(f"正在运行第 {idx + 1}/{NUM_RUNS_TIMES} 次测试")
        response = chat(
            model="llama3.1:8b",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": USER_PROMPT},
            ],
            options={"temperature": 0.3},
        )
        output_text = response.message.content
        final_answer = extract_final_answer(output_text)
        if final_answer.strip() == EXPECTED_OUTPUT.strip():
            print("SUCCESS")
            return True
        else:
            print(f"预期输出：{EXPECTED_OUTPUT}")
            print(f"实际输出：{final_answer}")
    return False


if __name__ == "__main__":
    test_your_prompt(YOUR_SYSTEM_PROMPT)


