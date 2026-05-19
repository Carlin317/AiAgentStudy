"""
[案例 03-6]operator.add 作为 Reducer(字符串):对字符串字段做拼接

知识点速览:
- Annotated[str, operator.add]:语义为字符串拼接,即 current + update.
- 适合多节点产出文本片段,最后拼成完整文案的场景.
"""

import operator
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END


class StringConcatState(TypedDict):
    text: Annotated[str, operator.add]


def add_text_1(state: StringConcatState) -> dict:
    return {"text": "Hello "}


def add_text_2(state: StringConcatState) -> dict:
    return {"text": "World!"}


def run_demo():
    print("3.2 字符串连接 Reducer 演示:")
    builder = StateGraph(StringConcatState)
    builder.add_node("add_text_1", add_text_1)
    builder.add_node("add_text_2", add_text_2)
    builder.add_edge(START, "add_text_1")
    builder.add_edge(START, "add_text_2")
    builder.add_edge("add_text_1", END)
    builder.add_edge("add_text_2", END)
    graph = builder.compile()
    result = graph.invoke({"text": "Say: "})
    print(f"初始状态: {{'text': 'Say: '}}")
    print(f"执行结果: {result}\n")


if __name__ == "__main__":
    run_demo()

"""
[输出示例]
3.2 字符串连接 Reducer 演示:
初始状态: {'text': 'Say: '}
执行结果: {'text': 'Say: Hello World!'}
"""
