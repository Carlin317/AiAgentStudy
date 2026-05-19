"""
[案例 04-22]从 JSON 文件加载提示词模板

对应教程章节:第 13 章 - 提示词与消息模板 → 8,从文件加载提示词(JSON / YAML)

知识点速览:
- 将 Prompt 放到 JSON/YAML 中,便于版本管理,多人协作和 A/B 测试
- load_prompt 根据文件内容加载模板对象,用法与 PromptTemplate 一致
- 注意当前工作目录与相对路径
"""

from langchain_core.prompts import load_prompt

template = load_prompt("prompt.json", encoding="utf-8")
print(template.format(name="张三", what="搞笑的"))

"""
[输出示例]
请张三讲一个搞笑的的故事
"""
