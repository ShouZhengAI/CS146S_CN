## LLM Prompt 演练场

练习 LLM 提示词工程的核心技术，这对于使用和理解编码型 LLM 至关重要。

# 第 1 周 — 提示词工程技术

你将通过设计提示词来完成特定任务，从而练习多种提示词工程技术。每个任务的说明都位于其相应的源文件顶部。

## 安装
请确保你已首先完成顶层 `README.md` 中描述的安装步骤。

## Ollama 安装
我们将使用一个名为 [Ollama](https://ollama.com/) 的工具，在你的本地机器上运行不同的最先进 LLM。请使用以下方法之一进行安装：

- macOS (Homebrew):
  ```bash
  brew install --cask ollama
  ollama serve
  ```

- Linux (推荐):
  ```bash
  curl -fsSL https://ollama.com/install.sh | sh
  ```

- Windows:
  从 [ollama.com/download](https://ollama.com/download) 下载并运行安装程序。

验证安装：
```bash
ollama -v
```

在运行测试脚本之前，请确保你已拉取以下模型。这只需要执行一次（除非你之后删除了这些模型）：
```bash
ollama run mistral-nemo:12b
ollama run llama3.1:8b
```

## 技术与源文件
- K-shot 提示 — `week1/k_shot_prompting.py`
- 思维链 (Chain-of-thought) — `week1/chain_of_thought.py`
- 工具调用 (Tool calling) — `week1/tool_calling.py`
- 自我一致性提示 (Self-consistency prompting) — `week1/self_consistency_prompting.py`
- RAG (检索增强生成) — `week1/rag.py`
- 反思 (Reflexion) — `week1/reflexion.py`

## 交付内容
- 阅读每个文件中的任务描述。
- 设计并运行提示词（查找代码中所有标记为 `TODO` 的位置）。这应该是你唯一需要修改的地方（即不要改动模型）。
- 迭代改进结果，直到测试脚本通过。
- 保存每种技术的最终提示词和输出。
- 确保在提交中包含每个提示词技术文件的完整代码。***请仔细检查所有 `TODO` 是否已解决。***

## 评分标准 (总计 60 分)
- 针对 6 种不同提示词技术中每个完成的提示词，各得 10 分。


🙏 Acknowledgement

[sweetkruts/cs146s](https://github.com/sweetkruts/cs146s)
