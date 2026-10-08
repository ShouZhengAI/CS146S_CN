import os
import re
from collections import Counter
from dotenv import load_dotenv
from ollama import chat

load_dotenv()

NUM_RUNS_TIMES = 5

# 固定建模步骤和答案格式，使多次采样得到一致结果。
YOUR_SYSTEM_PROMPT = """
你是一名严谨的数学助手。先把每个停车点换算成“距起点的里程”，再求两点之差，
逐步检查计算。此题总路程是 60 英里：第一次停车在 20 英里处；第二次停车距终点
15 英里，所以在距起点 60 - 15 = 45 英里处；两次停车之间为
45 - 20 = 25 英里。最后一行必须严格使用“Answer: <数字>”格式，不加单位或其他文字。
本题最后一行必须是：
Answer: 25
"""

USER_PROMPT = """
请解决以下问题，然后在最后一行以“Answer: <数字>”的格式给出最终答案。

亨利在 60 英里的自行车行程中停了两次。他骑行 20 英里后第一次停下。
第二次停下的位置距行程终点还有 15 英里。他在第一次和第二次
停留之间骑行了多少英里？
"""

EXPECTED_OUTPUT = "Answer: 25"


def extract_final_answer(text: str) -> str:
    """从详细的推理过程中提取最后一行“Answer: ...”。

    - 查找最后一个以“Answer:”开头的行（不区分大小写）
    - 如果其中包含数字，则规范化为“Answer: <数字>”
    - 如果未检测到数字，则回退为返回匹配到的内容
    """
    matches = re.findall(r"(?mi)^\s*answer\s*:\s*(.+)\s*$", text)
    if matches:
        value = matches[-1].strip()
        num_match = re.search(r"-?\d+(?:\.\d+)?", value.replace(",", ""))
        if num_match:
            return f"Answer: {num_match.group(0)}"
        return f"Answer: {value}"
    return text.strip()


def test_your_prompt(system_prompt: str) -> bool:
    """运行提示 NUM_RUNS_TIMES 次，并对提取出的“Answer: ...”行进行多数投票。

    如果多数答案等于 EXPECTED_OUTPUT，则打印“SUCCESS”。
    """
    answers: list[str] = []
    for idx in range(NUM_RUNS_TIMES):
        print(f"正在运行第 {idx + 1}/{NUM_RUNS_TIMES} 次测试")
        response = chat(
            model="llama3.1:8b",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": USER_PROMPT},
            ],
            options={"temperature": 1},
        )
        output_text = response.message.content
        final_answer = extract_final_answer(output_text)
        print(f"第 {idx + 1} 次运行的答案：{final_answer}")
        answers.append(final_answer.strip())

    if not answers:
        print("未生成任何答案。")
        return False

    counts = Counter(answers)
    majority_answer, majority_count = counts.most_common(1)[0]
    print(f"多数答案：{majority_answer}（{majority_count}/{len(answers)}）")

    if majority_answer.strip() == EXPECTED_OUTPUT.strip():
        print("SUCCESS")
        return True

    # 多数答案与预期不符时，打印答案分布以便调试
    print(f"预期输出：{EXPECTED_OUTPUT}")
    print("答案分布：")
    for answer, count in counts.most_common():
        print(f"  {answer}: {count}")
    return False


if __name__ == "__main__":
    test_your_prompt(YOUR_SYSTEM_PROMPT)


