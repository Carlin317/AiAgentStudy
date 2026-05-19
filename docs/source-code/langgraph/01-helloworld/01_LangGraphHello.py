"""
[案例 01-1]LangGraph 最简 HelloWorld:用"State + Nodes + Edges + Graph"构建一张最小线性图(START → greeting → add_emoji → END)

知识点速览:
- State:用 TypedDict 定义状态字段(如 name,greeting),图运行过程中保存的数据结构.
- Nodes:每个节点是一个函数,接收当前 state,返回对 state 的"部分更新"字典.
- Edges:add_edge 定义执行顺序;START / END 为虚拟起止节点.
- Graph API 主流程:定义 State → 定义节点函数 → StateGraph(State) → add_node / add_edge → compile() → invoke(initial_state).
- 可视化:compile() 后可通过 get_graph().print_ascii() 和 draw_mermaid() 查看图结构;__start__,__end__ 是内置虚拟节点名.
"""

from typing import TypedDict
from langgraph.graph import StateGraph, START, END
import uuid


# ========== 1. 定义 State ==========
class HelloState(TypedDict):
    name: str
    greeting: str


# ========== 2. 定义节点函数 ==========
def greet(hello_state: HelloState) -> dict:
    name = hello_state["name"]
    return {"greeting": f"你好,{name}"}


def add_emoji(hello_state: HelloState) -> dict:
    greeting = hello_state["greeting"]
    return {"greeting": greeting + "  ...😄"}


# ========== 3. 构建图 ==========
graph = StateGraph(HelloState)
graph.add_node("greeting", greet)
graph.add_node("add_emoji", add_emoji)
graph.add_edge(START, "greeting")
graph.add_edge("greeting", "add_emoji")
graph.add_edge("add_emoji", END)


# ========== 4. 编译 ==========
app = graph.compile()

# ========== 5. 运行 ==========
result = app.invoke({"name": "z3"})
print(result)
print(result["greeting"])

# ========== 6. 可视化 ==========
print(app.get_graph().print_ascii())
print("=" * 50)
print(app.get_graph().draw_mermaid())
print("=" * 50)

# 可选:生成 PNG 图片(依赖 mermaid.ink 或 Pyppeteer)
png_bytes = app.get_graph().draw_mermaid_png(max_retries=2, retry_delay=2.0)
output_path = "langgraph" + str(uuid.uuid4())[:8] + ".png"
with open(output_path, "wb") as f:
    f.write(png_bytes)
print(f"图片已生成:{output_path}")

"""
[输出示例]
{'name': 'z3', 'greeting': '你好,z3  ...😄'}
你好,z3  ...😄
+-----------+
| __start__ |
+-----------+
      *
      *
      *
+----------+
| greeting |
+----------+
      *
      *
      *
+-----------+
| add_emoji |
+-----------+
      *
      *
      *
 +---------+
 | __end__ |
 +---------+
None
==================================================
---
config:
  flowchart:
    curve: linear
---
graph TD;
        __start__([<p>__start__</p>]):::first
        greeting(greeting)
        add_emoji(add_emoji)
        __end__([<p>__end__</p>]):::last
        __start__ --> greeting;
        greeting --> add_emoji;
        add_emoji --> __end__;
        classDef default fill:#f2f0ff,line-height:1.2
        classDef first fill-opacity:0
        classDef last fill:#bfb6fc
"""
