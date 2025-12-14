# CS146S: 现代软件开发者 课程作业

这里是 [CS146S: 现代软件开发者](https://themodernsoftware.dev) 课程作业的主页，该课程将于 2025 年秋季在斯坦福大学教授。

## 仓库设置
以下步骤适用于 Python 3.12。

1.  安装 Anaconda
    -   下载并安装：[Anaconda 个人版](https://www.anaconda.com/download)
    -   打开一个新的终端，以便 `conda` 位于你的 `PATH` 环境变量中。

2.  创建并激活 Conda 环境 (Python 3.12)
    ```bash
    conda create -n cs146s python=3.12 -y
    conda activate cs146s
    ```

3.  安装 Poetry
    ```bash
    curl -sSL https://install.python-poetry.org | python -
    ```

4.  使用 Poetry 安装项目依赖（在已激活的 Conda 环境中）从**仓库根目录(CS146S_CN/Assignments)**：
    ```bash
    poetry install --no-interaction
    ```