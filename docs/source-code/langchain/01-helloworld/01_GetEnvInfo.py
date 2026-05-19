"""
[案例 01-1]环境检查:LangChain 版本与安装路径

对应教程章节:第 10 章 - LangChain 快速上手与 HelloWorld → 3,安装依赖

知识点速览:
- 通过 __version__ 和 __file__ 快速确认包版本与安装路径
- 用 sys.executable 排查虚拟环境 / 解释器不一致问题
- 无需 API Key,可直接运行
"""

import langchain
import langchain_community
import sys

print("langchainVersion:  " + langchain.__version__)
print("langchain_communityVersion:  " + langchain_community.__version__)
# 确认包来自当前虚拟环境而非全局安装
print("langchainfile:" + langchain.__file__)

print(sys.version)
# 排查"包装到了 A 环境,但运行走了 B 环境"的问题
print("pythonExecutable:" + sys.executable)

"""
[输出示例]
 langchainVersion:  1.2.9
 langchain_communityVersion:  0.4.1
 langchainfile:/Users/tools/PyCharmMiscProject/python100/.venv/lib/python3.10/site-packages/langchain/__init__.py
 3.10.19 (main, Oct  9 2025, 15:25:03) [Clang 17.0.0 (clang-1700.6.3.2)]
 pythonExecutable:/Users/tools/PyCharmMiscProject/python100/.venv/bin/python
"""
