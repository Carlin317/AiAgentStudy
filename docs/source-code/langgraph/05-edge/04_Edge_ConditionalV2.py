"""
[案例 05-4]条件边(字符串路由键):路由函数返回字符串 key,在 mapping 中映射到不同节点

知识点速览:
- add_conditional_edges(START, route_fn, {"key1": "node1", ...}):路由函数返回字符串与 mapping 的 key 匹配.
- 适合多分支入口:根据初始 state 决定第一跳.
"""

from langgraph.graph import StateGraph, START, END
from typing import TypedDict, List, Annotated


# ========== 1. 定义状态与节点 ==========
class DiliState(TypedDict):
    x: int


def addition1(state):
    print(f"addition1 收到: {state}")
    return {"x": state["x"] + 1}


def addition2(state):
    print(f"addition2 收到: {state}")
    return {"x": state["x"] + 2}


def addition3(state):
    print(f"addition3 收到: {state}")
    return {"x": state["x"] + 3}


def route_by_sentiment(state: DiliState) -> str:
    flag = state["x"]
    if flag == 1:
        return "condition_1"
    elif flag == 2:
        return "condition_2"
    else:
        return "condition_3"


# ========== 2. 构建图 ==========
graph = StateGraph(DiliState)
graph.add_node("node1", addition1)
graph.add_node("node2", addition2)
graph.add_node("node3", addition3)

graph.add_conditional_edges(
    START,
    route_by_sentiment,
    {"condition_1": "node1", "condition_2": "node2", "condition_3": "node3"},
)

graph.add_edge("node1", END)
graph.add_edge("node2", END)
graph.add_edge("node3", END)
# ========== 3. 编译并执行 ==========
app = graph.compile()
initial_state = {"x": 3}
result = app.invoke(initial_state)
print(f"最后的结果是: {result}")

print(app.get_graph().print_ascii())
print("=================================")
print()
print(app.get_graph().draw_mermaid())

"""
[输出示例]
addition3 收到: {'x': 3}
最后的结果是: {'x': 6}
                +-----------+                  
                | __start__ |                  
                +-----------+..                
             ...      .        ...             
          ...         .           ...          
        ..            .              ..        
+-------+         +-------+         +-------+  
| node1 |*        | node2 |         | node3 |  
+-------+ ***     +-------+       **+-------+  
             ***      *        ***             
                ***   *     ***                
                   ** *   **                   
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
        node1(node1)
        node2(node2)
        node3(node3)
        __end__([<p>__end__</p>]):::last
        __start__ -. &nbsp;condition_1&nbsp; .-> node1;
        __start__ -. &nbsp;condition_2&nbsp; .-> node2;
        __start__ -. &nbsp;condition_3&nbsp; .-> node3;
        node1 --> __end__;
        node2 --> __end__;
        node3 --> __end__;
        classDef default fill:#f2f0ff,line-height:1.2
        classDef first fill-opacity:0
        classDef last fill:#bfb6fc
"""
