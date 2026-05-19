"""
[案例 05-5]条件入口点:从 START 开始就根据初始输入分支到不同处理节点

知识点速览:
- add_conditional_edges(START, route_fn, mapping):invoke 传入的 state 先交给 route_fn,返回值在 mapping 中查下一节点.
- 与条件边的区别:条件边是节点执行完后分支;条件入口点是图一启动就分支,常用于一级路由.
"""

from typing import TypedDict
from langgraph.graph import StateGraph, START, END


# ========== 1. 定义状态 ==========
class SimpleState(TypedDict):
    user_input: str
    response: str
    node_visited: str


# ========== 2. 路由函数 ==========
def route_input(state: SimpleState) -> str:
    text = state["user_input"].lower()

    if "hello" in text or "hi" in text:
        return "greeting"
    elif "bye" in text or "exit" in text:
        return "farewell"
    else:
        return "question"


# ========== 3. 处理节点 ==========
def handle_greeting(state: SimpleState) -> SimpleState:
    state["response"] = "你好!很高兴见到你!"
    state["node_visited"] = "greeting_node"
    return state


def handle_farewell(state: SimpleState) -> SimpleState:
    state["response"] = "再见!祝你有个美好的一天!"
    state["node_visited"] = "farewell_node"
    return state


def handle_question(state: SimpleState) -> SimpleState:
    state["response"] = "我听到了你的问题,需要更多帮助吗?"
    state["node_visited"] = "question_node"
    return state


# ========== 4. 构建图 ==========
def create_simple_graph():
    state_graph = StateGraph(SimpleState)

    state_graph.add_node("greeting_node", handle_greeting)
    state_graph.add_node("farewell_node", handle_farewell)
    state_graph.add_node("question_node", handle_question)

    state_graph.add_conditional_edges(
        START,
        route_input,
        {
            "greeting": "greeting_node",
            "farewell": "farewell_node",
            "question": "question_node",
        },
    )

    state_graph.add_edge("greeting_node", END)
    state_graph.add_edge("farewell_node", END)
    state_graph.add_edge("question_node", END)

    return state_graph.compile()


# ========== 5. 执行示例 ==========
def run_example():
    graph = create_simple_graph()
    test_inputs = ["Hello everyone!", "Goodbye now", "What time is it?"]

    for user_input in test_inputs:
        print(f"\n输入: {user_input}")
        print("-" * 30)

        initial_state = SimpleState(user_input=user_input, response="", node_visited="")
        result = graph.invoke(initial_state)

        print(f"路由决策: {route_input(initial_state)}")
        print(f"访问的节点: {result['node_visited']}")
        print(f"响应: {result['response']}")

    print()
    print(graph.get_graph().print_ascii())
    print("=================================")
    print()
    print(graph.get_graph().draw_mermaid())


if __name__ == "__main__":
    print("简单条件入口点示例")
    print("=" * 40)
    run_example()


"""
[输出示例]
简单条件入口点示例
========================================

输入: Hello everyone!
------------------------------
路由决策: greeting
访问的节点: greeting_node
响应: 你好!很高兴见到你!

输入: Goodbye now
------------------------------
路由决策: farewell
访问的节点: farewell_node
响应: 再见!祝你有个美好的一天!

输入: What time is it?
------------------------------
路由决策: question
访问的节点: question_node
响应: 我听到了你的问题,需要更多帮助吗?

                              +-----------+                                
                              | __start__ |.                               
                         .....+-----------+ .....                          
                     ....           .            ....                      
                .....               .                .....                 
             ...                    .                     ...              
+---------------+           +---------------+           +---------------+  
| farewell_node |           | greeting_node |           | question_node |  
+---------------+****       +---------------+        ***+---------------+  
                     ****           *            ****                      
                         *****      *       *****                          
                              ***   *    ***                               
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
        greeting_node(greeting_node)
        farewell_node(farewell_node)
        question_node(question_node)
        __end__([<p>__end__</p>]):::last
        __start__ -. &nbsp;farewell&nbsp; .-> farewell_node;
        __start__ -. &nbsp;greeting&nbsp; .-> greeting_node;
        __start__ -. &nbsp;question&nbsp; .-> question_node;
        farewell_node --> __end__;
        greeting_node --> __end__;
        question_node --> __end__;
        classDef default fill:#f2f0ff,line-height:1.2
        classDef first fill-opacity:0
        classDef last fill:#bfb6fc
"""
