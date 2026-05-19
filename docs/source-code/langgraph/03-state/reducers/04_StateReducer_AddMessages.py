"""
[案例 03-4]add_messages Reducer:消息列表专用,节点只返回增量消息,自动追加到 state["messages"]

知识点速览:
- Annotated[List, add_messages]:新消息追加到列表末尾而非覆盖.
- 节点返回格式可为 [("role", content)] 或 [AIMessage/HumanMessage] 等,由 add_messages 统一合并.
- 并行分支下的消息合并顺序由框架决定,不应作为业务契约.
"""

from typing import Annotated, List
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages


class AddMessagesState(TypedDict):
    messages: Annotated[List, add_messages]


def chat_node_1(state: AddMessagesState) -> dict:
    return {"messages": [("assistant", "Hello from node 1")]}


def chat_node_2(state: AddMessagesState) -> dict:
    return {"messages": [("assistant", "Hello from node 2")]}


def run_demo():
    print("2. add_messages Reducer(消息列表专用)演示:")
    builder = StateGraph(AddMessagesState)
    builder.add_node("chat1", chat_node_1)
    builder.add_node("chat2", chat_node_2)
    builder.add_edge(START, "chat1")
    builder.add_edge(START, "chat2")  # 两节点并行,各自追加消息
    builder.add_edge("chat1", END)
    builder.add_edge("chat2", END)
    graph = builder.compile()

    result = graph.invoke({"messages": [("user", "Hi there!")]})
    print(f"初始状态: {{'messages': [('user', 'Hi there!')]}}")
    print(f"执行结果: {result}\n")
    print("*" * 60)
    print(graph.get_graph().print_ascii())


if __name__ == "__main__":
    run_demo()

"""
[输出示例]
2. add_messages Reducer(消息列表专用)演示:
初始状态: {'messages': [('user', 'Hi there!')]}
执行结果: {'messages': [HumanMessage(content='Hi there!', additional_kwargs={}, response_metadata={}, id='1ef23c0c-ec9a-4e41-a3fb-2a80e5f84666'), AIMessage(content='Hello from node 1', additional_kwargs={}, response_metadata={}, id='09bed348-3770-400b-93fd-f550a647445f', tool_calls=[], invalid_tool_calls=[]), AIMessage(content='Hello from node 2', additional_kwargs={}, response_metadata={}, id='06bbf85f-9661-450d-a54e-5025abe7a34b', tool_calls=[], invalid_tool_calls=[])]}

************************************************************
       +-----------+         
       | __start__ |         
       +-----------+         
         *        *          
       **          **        
      *              *       
+-------+         +-------+  
| chat1 |         | chat2 |  
+-------+         +-------+  
         *        *          
          **    **           
            *  *             
        +---------+          
        | __end__ |          
        +---------+          
None
"""
