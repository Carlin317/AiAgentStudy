“””
【案例 07-11】代理节点调用子图：父子 State 字段完全不同时，在父图节点里手动构造子图输入、
invoke 子图、再把结果写回父 State。

对应教程章节：第 25 章 - LangGraph 高级特性 → 4、子图（Subgraphs）

知识点速览：
- 父子状态无交集字段时，必须用「代理节点」做父→子、子→父的状态转换。
- 代理节点签名仍为 (父 state) -> 父 state 增量；内部调用 compiled_subgraph.invoke(subgraph_input)。
- 该模式可扩展任意形状的状态转换，是多智能体、流水线拆图时的常用技巧。
“””

from typing import TypedDict

from langgraph.graph import StateGraph, START, END


# ========== 1. 状态定义 ==========
class ParentState(TypedDict):
    user_query: str
    final_answer: str | None


class SubgraphState(TypedDict):
    analysis_input: str
    analysis_result: str
    intermediate_steps: list


# ========== 2. 子图 ==========
def subgraph_analysis_node(state: SubgraphState) -> SubgraphState:
    query = state["analysis_input"]
    state["intermediate_steps"] = [f"解析查询：{query}", "执行分析逻辑", "生成结果"]
    state["analysis_result"] = f"针对「{query}」的分析结果：这是子图处理后的内容"
    return state


def build_subgraph() -> StateGraph:
    sub_builder = StateGraph(SubgraphState)
    sub_builder.add_node("subgraph_analysis_node", subgraph_analysis_node)
    sub_builder.add_edge(START, "subgraph_analysis_node")
    sub_builder.add_edge("subgraph_analysis_node", END)
    return sub_builder.compile()


compiled_subgraph = build_subgraph()


# ========== 3. 父图代理节点 ==========
def call_subgraph_proxy(state: ParentState) -> ParentState:
    """父→子状态转换 → invoke 子图 → 子→父结果回写。"""
    subgraph_input = {
        "analysis_input": state["user_query"],
        "intermediate_steps": [],
        "analysis_result": "",
    }

    subgraph_response = compiled_subgraph.invoke(subgraph_input)

    return {
        "user_query": state["user_query"],
        "final_answer": subgraph_response["analysis_result"],
    }


# ========== 4. 构建父图 ==========
def build_parent_graph():
    parent_builder = StateGraph(ParentState)
    parent_builder.add_node("call_subgraph_proxy", call_subgraph_proxy)
    parent_builder.add_edge(START, "call_subgraph_proxy")
    parent_builder.add_edge("call_subgraph_proxy", END)
    return parent_builder.compile()


# ========== 5. 执行 ==========
def main():
    parent_graph = build_parent_graph()

    initial_state = {
        "user_query": "请分析Python中StateGraph的使用场景",
        "final_answer": None,
    }
    print("父图初始状态：", initial_state)

    final_state = parent_graph.invoke(initial_state)

    print("\n父图最终状态：", final_state)
    print("\n子图处理后的最终答案：", final_state["final_answer"])


if __name__ == "__main__":
    main()

"""
【输出示例】
父图初始状态： {'user_query': '请分析Python中StateGraph的使用场景', 'final_answer': None}

父图最终状态： {'user_query': '请分析Python中StateGraph的使用场景', 'final_answer': '针对「请分析Python中StateGraph的使用场景」的分析结果：这是子图处理后的内容'}

子图处理后的最终答案： 针对「请分析Python中StateGraph的使用场景」的分析结果：这是子图处理后的内容
"""
