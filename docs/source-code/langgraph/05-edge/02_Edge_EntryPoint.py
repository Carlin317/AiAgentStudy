"""
[案例 05-2]入口点与出口点:set_entry_point / set_finish_point,等价于 add_edge(START, node) 与 add_edge(node, END)

知识点速览:
- set_entry_point(node_id):底层等价于 add_edge(START, node_id).
- set_finish_point(node_id):底层等价于 add_edge(node_id, END).
- 适合单入口单出口的图,减少重复写 START/END 边.
"""

from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END


# ========== 1. 定义状态与节点 ==========
class DiliState(TypedDict):
    value: int
    step: str


def node_a(state: DiliState) -> dict:
    print("执行节点A")
    print("state[value]:" + str(state["value"]))
    print("state[step]:" + str(state["step"]))
    return {"value": state["value"] + 1, "step": "A执行完毕"}


def node_b(state: DiliState) -> dict:
    print("执行节点B")
    return {"value": state["value"] * 2, "step": "B执行完毕"}


# ========== 2. 构建并执行 ==========
def main():
    print("=== 入口点演示 ===")

    builder = StateGraph(DiliState)
    builder.add_node("node_a", node_a)
    builder.add_node("node_b", node_b)

    builder.set_entry_point("node_a")
    builder.add_edge("node_a", "node_b")
    builder.set_finish_point("node_b")

    graph = builder.compile()
    result = graph.invoke({"value": 0, "step": "hello"})
    print(f"执行结果: {result}\n")

    print()
    print(graph.get_graph().print_ascii())
    print("=================================")
    print()
    print(graph.get_graph().draw_mermaid())


if __name__ == "__main__":
    main()

"""
[输出示例]
=== 入口点演示 ===
执行节点A
state[value]:0
state[step]:hello
执行节点B
执行结果: {'value': 2, 'step': 'B执行完毕'}


+-----------+  
| __start__ |  
+-----------+  
      *        
      *        
      *        
  +--------+   
  | node_a |   
  +--------+   
      *        
      *        
      *        
  +--------+   
  | node_b |   
  +--------+   
      *        
      *        
      *        
 +---------+   
 | __end__ |   
 +---------+   
None
=================================

---
config:
  flowchart:
    curve: linear
---
graph TD;
        __start__([<p>__start__</p>]):::first
        node_a(node_a)
        node_b(node_b)
        __end__([<p>__end__</p>]):::last
        __start__ --> node_a;
        node_a --> node_b;
        node_b --> __end__;
        classDef default fill:#f2f0ff,line-height:1.2
        classDef first fill-opacity:0
        classDef last fill:#bfb6fc
"""
