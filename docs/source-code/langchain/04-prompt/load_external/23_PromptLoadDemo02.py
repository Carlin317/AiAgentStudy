"""
[案例 04-23]从 YAML 文件加载提示词模板

对应教程章节:第 13 章 - 提示词与消息模板 → 8,从文件加载提示词(JSON / YAML)

知识点速览:
- 与 JSON 版本用法一致,YAML 格式更适合人读和写注释
- load_prompt 自动识别文件格式
"""

import warnings

warnings.filterwarnings(
    "ignore", message="Core Pydantic V1 functionality isn't compatible with Python 3.14"
)

from langchain_core.prompts import load_prompt

template = load_prompt("prompt.yaml", encoding="utf-8")
print(template.format(name="年轻人", what="滑稽"))
#

"""
[输出示例]
请年轻人讲一个滑稽的故事
"""
