"""
[案例 03-10]多种 Reducer 并存:messages 用 add_messages,tags 用 operator.add 拼接列表,score 用 operator.add 做数值累加

知识点速览:
- 同一份 State 里不同字段可配置不同 Reducer:字段定义是一层,合并方式是另一层.
- add_messages:增量追加;operator.add 作用于列表时拼接,作用于 float 时加法累加.
- invoke 里可传 OpenAI 风格的 {"role", "content"} 字典,运行时会转为 Message 对象.
"""

from typing import Annotated, List

import operator
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from typing_extensions import TypedDict


class ChatState(TypedDict):
    messages: Annotated[List, add_messages]       # 追加语义
    tags: Annotated[List[str], operator.add]      # 列表拼接
    score: Annotated[float, operator.add]         # 数值累加


def process_user_message(state: ChatState) -> dict:
    # dict 入参在运行时已转为 HumanMessage 等对象,须用 .content 读正文
    user_message = state["messages"][-1]
    return {
        "messages": [("assistant", f"Echo: {user_message.content}")],
        "tags": ["processed"],
        "score": 1.0,
    }


def add_sentiment_tag(state: ChatState) -> dict:
    return {"tags": ["positive"], "score": 0.5}


def run_demo():
    builder = StateGraph(ChatState)
    builder.add_node("process", process_user_message)
    builder.add_node("sentiment", add_sentiment_tag)

    # 两节点从 START 并行
    builder.add_edge(START, "process")
    builder.add_edge(START, "sentiment")
    builder.add_edge("process", END)
    builder.add_edge("sentiment", END)

    graph = builder.compile()

    result = graph.invoke(
        {
            "messages": [{"role": "user", "content": "Hello, how are you?"}],
            "tags": ["greeting"],
            "score": 0.0,
        }
    )
    print(result)


if __name__ == "__main__":
    run_demo()

"""
[输出示例]
{'messages': [HumanMessage(content='Hello, how are you?', additional_kwargs={}, response_metadata={}, id='4350252b-ace7-429a-8cc8-67d232d91f42'), AIMessage(content='Echo: Hello, how are you?', additional_kwargs={}, response_metadata={}, id='ab394788-89d0-45f2-a6b0-5252a448ebb1', tool_calls=[], invalid_tool_calls=[])], 'tags': ['greeting', 'processed', 'positive'], 'score': 1.5}
"""
