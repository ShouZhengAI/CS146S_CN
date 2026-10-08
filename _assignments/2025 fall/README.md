# CS146S：现代软件开发者——课程作业

这里存放斯坦福大学 2025 年秋季学期课程 [CS146S：现代软件开发者](https://themodernsoftware.dev) 的作业。

## 仓库配置
以下步骤适用于 Python 3.12。

1. 安装 Anaconda
   - 下载并安装：[Anaconda 个人版](https://www.anaconda.com/download)
   - 打开一个新的终端，确保可通过 `PATH` 找到 `conda`。

2. 创建并激活 Conda 环境（Python 3.12）
   ```bash
   conda create -n cs146s python=3.12 -y
   conda activate cs146s
   ```

3. 安装 Poetry
   ```bash
   curl -sSL https://install.python-poetry.org | python -
   ```

4. 使用 Poetry 安装项目依赖（在已激活的 Conda 环境中）
   在仓库根目录下运行：
   ```bash
   poetry install --no-interaction
   ```