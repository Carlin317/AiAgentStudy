"""
[案例 05-5]JsonOutputParser + get_format_instructions():用格式说明引导模型输出

对应教程章节:第 14 章 - 输出解析器 → 2,常用输出解析器用法

知识点速览:
- get_format_instructions() 返回一段格式说明,描述期望的 JSON 结构(键名,类型等)
- 将说明拼入 Prompt 的 {format_instructions} 占位符,可显著降低模型输出格式错误的概率
- 绑定 Pydantic 模型后 get_format_instructions() 会自动根据 schema 生成说明
- 当前 JsonOutputParser 解析结果仍为 dict;若需 Pydantic 实例,见 StructuredOutput_Pydantic.py
"""

from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate
import os
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from loguru import logger
from pydantic import BaseModel, Field

load_dotenv(encoding="utf-8")


class Person(BaseModel):
    """新闻条目结构:时间,人物,事件."""

    time: str = Field(description="时间")
    person: str = Field(description="人物")
    event: str = Field(description="事件")


# ========== 1. 创建解析器并获取格式说明 ==========
parser = JsonOutputParser(pydantic_object=Person)
format_instructions = parser.get_format_instructions()

# ========== 2. 构造对话模板 ==========
chat_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "你是一个AI助手,你只能输出结构化JSON数据."),
        ("human", "请生成一个关于{topic}的新闻.{format_instructions}"),
    ]
)

prompt = chat_prompt.format_messages(
    topic="小米SU7", format_instructions=format_instructions
)
logger.info(prompt)

# ========== 3. 初始化大模型 ==========
model = init_chat_model(
    model="qwen-plus",
    model_provider="openai",
    api_key=os.getenv("aliQwen-api"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

# ========== 4. 调用模型并解析 ==========
result = model.invoke(prompt)
logger.info(f"模型原始输出:\n{result}")

response = parser.invoke(result)
logger.info(f"解析后的结构化结果:\n{response}")
logger.info(f"结果类型: {type(response)}")
