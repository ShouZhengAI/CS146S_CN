# 第 1 周——提示技术

你将通过编写提示词来完成特定任务，从而练习多种提示技术。每项任务的说明均位于对应源文件的顶部。

## 安装
请确保你已先按照顶层 `README.md` 中的说明完成安装。

## 安装 Ollama
我们将使用 [Ollama](https://ollama.com/) 在你的计算机上本地运行不同的先进大语言模型。请选择以下任一安装方式：

- macOS（Homebrew）：
  ```bash
  brew install --cask ollama 
  ollama serve
  ```

- Linux（推荐）：
  ```bash
  curl -fsSL https://ollama.com/install.sh | sh
  ```

- Windows：
  从 [ollama.com/download](https://ollama.com/download) 下载安装程序并运行。

验证安装：
```bash
ollama -v
```

运行测试脚本之前，请确保已拉取以下模型。此操作只需执行一次（除非之后删除了这些模型）：
```bash
ollama run mistral-nemo:12b
ollama run llama3.1:8b
```

## 技术与源文件
- K 样本提示——`week1/k_shot_prompting.py`
- 思维链——`week1/chain_of_thought.py`
- 工具调用——`week1/tool_calling.py`
- 自洽性提示——`week1/self_consistency_prompting.py`
- RAG（检索增强生成）——`week1/rag.py`
- 反思——`week1/reflexion.py`

## 提交内容
- 阅读每个文件中的任务说明。
- 设计并运行提示词（查找代码中所有标有 `TODO` 的位置）。这应是你唯一需要修改的内容（即不要调整模型）。
- 反复迭代以改善结果，直至测试脚本通过。
- 保存每种技术最终使用的提示词及输出。
- 提交内容中务必包含每个提示技术文件的完整代码。***请再次确认所有 `TODO` 均已解决。***

## 评分标准（总计 60 分）
- 六种不同提示技术中，每完成一个提示词得 10 分