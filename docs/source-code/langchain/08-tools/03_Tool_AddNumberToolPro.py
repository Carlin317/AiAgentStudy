"""
【案例 08-3】加法工具（Pydantic 版）：用 args_schema 绑定参数模型

对应教程章节：第 17 章 - Tools 工具调用 → 4、参数 schema：为什么要配合 Pydantic

知识点速览：
- args_schema 将参数语义说明显式暴露给模型，提升参数生成正确率
- Field 的 description 会进入工具参数 schema，模型可据此理解每个参数的含义
- 工具整体用途说明仍应写在函数 docstring 中
"""
from langchain_core.tools import tool
from loguru import logger
from pydantic import BaseModel, Field


class AddNumberInput(BaseModel):
    """加法运算参数结构"""

    a: int = Field(description="第1个参数")
    b: int = Field(description="第2个参数")


@tool(args_schema=AddNumberInput)
def add_number(a: int, b: int) -> int:
    """计算两个整数之和"""
    return a + b


# ========== 1. 查看工具属性 ==========
logger.info(f"name = {add_number.name}")
logger.info(f"args = {add_number.args}")
logger.info(f"description = {add_number.description}")
logger.info(f"return_direct = {add_number.return_direct}")

# ========== 2. 调用工具 ==========
res = add_number.invoke({"a": 1, "b": 2})
logger.info(res)
