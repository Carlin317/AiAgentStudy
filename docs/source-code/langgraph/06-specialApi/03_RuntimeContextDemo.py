"""
[案例 06-3]Runtime 与 context_schema:创建图时传入 context_schema,invoke 时传入 context,
节点函数接收 (state, runtime),通过 runtime.context 访问配置,实现"配置与状态分离".

对应教程章节:第 24 章 - LangGraph API:节点,边与进阶 → 3,Send,Command 与 Runtime 上下文

知识点速览:
- StateGraph(State, context_schema=ContextSchema):运行时配置不进入 state,适合放模型名,连接串,密钥等.
- 节点签名 (state, runtime: Runtime[ContextSchema]):runtime.context 即 invoke 时传入的配置对象,类型安全.
- 核心意识:业务数据走 State,环境配置走 Runtime Context.
"""

from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.runtime import Runtime
from langchain_core.messages import AIMessage, HumanMessage
from dataclasses import dataclass


# ========== 1. 状态与上下文定义 ==========
class AgentState(TypedDict):
    messages: Annotated[list, lambda x, y: x + y]
    response: str


@dataclass
class ContextSchema:
    model_name: str
    db_connection: str
    api_key: str


# ========== 2. 节点函数 ==========
def process_message(state: AgentState, runtime: Runtime[ContextSchema]) -> dict:
    print("执行节点: process_message")

    last_message = state["messages"][-1].content if state["messages"] else ""
    print(f"用户消息: {last_message}")
    print("========== 从 RuntimeContext 获取配置 ==========")
    model_name = runtime.context.model_name
    db_connection = runtime.context.db_connection
    api_key = runtime.context.api_key

    print(f"使用的模型: {model_name}")
    print(f"数据库连接: {db_connection}")
    print(f"API密钥前缀: {api_key[:5]}***")

    response = f"使用 {model_name} 处理了您的请求,已连接到 {db_connection}"

    return {"messages": [AIMessage(content=response)], "response": response}


def generate_response(state: AgentState, runtime: Runtime[ContextSchema]) -> dict:
    print("执行节点: generate_response")

    model_name = runtime.context.model_name
    print(f"使用模型 {model_name} 生成最终响应")

    previous_response = state["response"]
    final_response = f"{previous_response}\n\n这是使用 {model_name} 生成的完整响应."

    return {"messages": [AIMessage(content=final_response)], "response": final_response}


# ========== 3. 构建与执行 ==========
def main():
    print("=== Context Schema 演示 ===\n")

    context = ContextSchema(
        model_name="gpt-4-turbo",
        db_connection="postgresql://user:pass@localhost:5432/orders_db",
        api_key="sk-abcdefghijklmnopqrstuvwxyz123456",
    )

    builder = StateGraph(AgentState, context_schema=ContextSchema)
    builder.add_node("process_message", process_message)
    builder.add_node("generate_response", generate_response)

    builder.add_edge(START, "process_message")
    builder.add_edge("process_message", "generate_response")
    builder.add_edge("generate_response", END)

    graph = builder.compile()

    initial_state = {
        "messages": [HumanMessage(content="请帮我查询最新的订单信息")],
        "response": "",
    }

    print("初始状态:", initial_state)
    print()
    print(
        "上下文信息:\n",
        {
            "model_name": context.model_name,
            "db_connection": context.db_connection,
            "api_key": f"{context.api_key[:5]}***",
        },
    )
    print("\n" + "-" * 50 + "\n")

    result = graph.invoke(initial_state, context=context)

    print("\n" + "=" * 50)
    print("最终状态:", result)
    print("\n最终响应:")
    print(result["response"])


if __name__ == "__main__":
    main()

"""
[输出示例]
=== Context Schema 演示 ===

初始状态: {'messages': [HumanMessage(content='请帮我查询最新的订单信息', additional_kwargs={}, response_metadata={})], 'response': ''}

上下文信息:
 {'model_name': 'gpt-4-turbo', 'db_connection': 'postgresql://user:pass@localhost:5432/orders_db', 'api_key': 'sk-ab***'}

--------------------------------------------------

执行节点: process_message
用户消息: 请帮我查询最新的订单信息
========== 从 RuntimeContext 获取配置 ==========
使用的模型: gpt-4-turbo
数据库连接: postgresql://user:pass@localhost:5432/orders_db
API密钥前缀: sk-ab***
执行节点: generate_response
使用模型 gpt-4-turbo 生成最终响应

==================================================
最终状态: {'messages': [HumanMessage(content='请帮我查询最新的订单信息', additional_kwargs={}, response_metadata={}), AIMessage(content='使用 gpt-4-turbo 处理了您的请求,已连接到 postgresql://user:pass@localhost:5432/orders_db', additional_kwargs={}, response_metadata={}, tool_calls=[], invalid_tool_calls=[]), AIMessage(content='使用 gpt-4-turbo 处理了您的请求,已连接到 postgresql://user:pass@localhost:5432/orders_db\n\n这是使用 gpt-4-turbo 生成的完整响应.', additional_kwargs={}, response_metadata={}, tool_calls=[], invalid_tool_calls=[])], 'response': '使用 gpt-4-turbo 处理了您的请求,已连接到 postgresql://user:pass@localhost:5432/orders_db\n\n这是使用 gpt-4-turbo 生成的完整响应.'}

最终响应:
使用 gpt-4-turbo 处理了您的请求,已连接到 postgresql://user:pass@localhost:5432/orders_db

这是使用 gpt-4-turbo 生成的完整响应.
"""
