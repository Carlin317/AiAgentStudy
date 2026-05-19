"""
[案例 03-2]图的输入/输出 Schema:用 input_schema 和 output_schema 限制调用方只能传 question,返回时只拿 answer

知识点速览:
- OverallState 是内部完整 State Schema,InputState / OutputState 是图对外暴露的输入输出契约.
- StateGraph(OverallState, input_schema=InputState, output_schema=OutputState):第一个参数描述内部完整状态,后两个限制边界 I/O.
- 节点内部围绕完整状态空间工作;只有"图的边界"受 input/output 约束.
"""

from langgraph.graph import StateGraph, START, END
from typing_extensions import TypedDict


# ========== 1. 定义 Schema ==========
class InputState(TypedDict):
    question: str


class OutputState(TypedDict):
    answer: str


class OverallState(InputState, OutputState):
    pass


# ========== 2. 定义节点函数 ==========
def answer_node(state: InputState):
    print(f"执行 answer_node 节点:")
    print(f"  输入: {state}")
    answer = "再见" if "bye" in state["question"].lower() else "你好"
    result = {"answer": answer, "question": state["question"]}
    print(f"  输出: {result}")
    return result


# ========== 3. 构建并执行 ==========
def demo_input_output_schema():
    print("=== 演示输入输出模式 ===")
    builder = StateGraph(
        OverallState, input_schema=InputState, output_schema=OutputState
    )
    builder.add_edge(START, "answer_node")
    builder.add_node("answer_node", answer_node)
    builder.add_edge("answer_node", END)
    graph = builder.compile()

    result = graph.invoke({"question": "你好"})
    print(f"图调用结果: {result}")
    print(graph.get_graph().print_ascii())
    print()


def main():
    print("=== LangGraph 图输入输出模式===\n")
    demo_input_output_schema()
    print("=== 演示完成 ===")


if __name__ == "__main__":
    main()

"""
[输出示例]
=== LangGraph 图输入输出模式===

=== 演示输入输出模式 ===
执行 answer_node 节点:
  输入: {'question': '你好'}
  输出: {'answer': '你好', 'question': '你好'}
图调用结果: {'answer': '你好'}
 +-----------+   
 | __start__ |   
 +-----------+   
        *        
        *        
        *        
+-------------+  
| answer_node |  
+-------------+  
        *        
        *        
        *        
  +---------+    
  | __end__ |    
  +---------+    
None

=== 演示完成 ===
"""
