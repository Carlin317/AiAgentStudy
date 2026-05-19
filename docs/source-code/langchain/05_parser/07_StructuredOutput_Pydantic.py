"""
[案例 05-7]PydanticOutputParser:用 Pydantic 模型定义输出结构并校验

对应教程章节:第 14 章 - 输出解析器 → 3,结构化输出(TypedDict / Pydantic / Annotated)

知识点速览:
- PydanticOutputParser 解析结果为 Pydantic 实例,可利用 field_validator 做运行时校验
- 与 JsonOutputParser 的区别:JsonOutputParser 返回 dict,PydanticOutputParser 返回强类型对象
- 适合需要强类型和校验失败明确报错的场景
"""

import os
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate
from loguru import logger
from pydantic import BaseModel, Field, field_validator

load_dotenv(encoding="utf-8")


class Product(BaseModel):
    """产品信息:名称,类别,简介."""

    name: str = Field(description="产品名称")
    category: str = Field(description="产品类别")
    description: str = Field(description="产品简介")

    @field_validator("description")
    def validate_description(cls, value):
        """description 长度必须 >= 10,否则抛 ValueError."""
        if len(value) < 10:
            raise ValueError("产品简介长度必须大于等于10")
        return value


# ========== 1. 创建解析器并获取格式说明 ==========
parser = PydanticOutputParser(pydantic_object=Product)
format_instructions = parser.get_format_instructions()

# ========== 2. 构造对话模板 ==========
prompt_template = ChatPromptTemplate.from_messages(
    [
        ("system", "你是一个AI助手,你只能输出结构化的json数据\n{format_instructions}"),
        ("human", "请你输出标题为:{topic}的新闻内容"),
    ]
)

prompt = prompt_template.format_messages(
    topic="华为Mate X7", format_instructions=format_instructions
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
logger.info(f"模型原始输出:\n{result.content}")

# 解析为 Product 实例,校验不通过会抛错
response = parser.invoke(result)
logger.info(f"解析后的结构化结果:\n{response}")
logger.info(f"结果类型: {type(response)}")  # <class '__main__.Product'>
