"""
[案例 07-5]多模式流式传输:同一图依次演示 values,updates,列表组合 [values, updates],以及 debug 模式.

对应教程章节:第 25 章 - LangGraph 高级特性 → 1,流式处理(Streaming)

知识点速览:
- stream_mode 为列表时,每次迭代得到 (mode, chunk) 元组,便于前端按类型分别处理.
- values 看全貌,updates 看增量;debug 适合调试,不适合业务输出.
- 同一张图可同时暴露多种观察视角.
"""

from typing import TypedDict

from langgraph.graph import StateGraph, START, END


class DiliState(TypedDict):
    question: str
    answer: str
    confidence: float  # 置信度分数
    steps: list


def think(state: DiliState) -> DiliState:
    question = state["question"]
    steps = [f"分析问题: {question}", "检索相关知识", "形成初步答案"]
    return {"steps": steps}


def respond(state: DiliState) -> DiliState:
    question = state["question"]
    if "天气" in question:
        answer = "今天天气晴朗"
        confidence = 0.9
    elif "时间" in question:
        answer = "现在是上午10点"
        confidence = 0.8
    else:
        answer = "这是一个很好的问题"
        confidence = 0.7

    return {
        "answer": answer,
        "confidence": confidence,
    }


def reflect(state: DiliState) -> DiliState:
    answer = state["answer"]
    confidence = state["confidence"]
    steps = state.get("steps", [])

    steps.append(f"验证答案: {answer}")
    steps.append(f"置信度评估: {confidence}")

    if confidence > 0.8:
        conclusion = "高置信度答案"
    elif confidence > 0.5:
        conclusion = "中等置信度答案"
    else:
        conclusion = "低置信度答案"

    steps.append(f"结论: {conclusion}")

    return {"steps": steps}


def main():
    builder = StateGraph(DiliState)
    builder.add_node("think", think)
    builder.add_node("respond", respond)
    builder.add_node("reflect", reflect)

    builder.add_edge(START, "think")
    builder.add_edge("think", "respond")
    builder.add_edge("respond", "reflect")
    builder.add_edge("reflect", END)

    graph = builder.compile()

    print("=== LangGraph 多模式流式传输演示 ===\n")

    input_state = {
        "question": "今天天气怎么样?",
        "answer": "",
        "confidence": 0.0,
        "steps": [],
    }

    print("========== 1. values 模式 ==========")
    for chunk in graph.stream(input_state, stream_mode="values"):
        print(f"  {chunk}")

    print("\n" + "=" * 60 + "\n")

    print("========== 2. updates 模式 ==========")
    for chunk in graph.stream(input_state, stream_mode="updates"):
        print(f"  {chunk}")

    print("\n" + "=" * 60 + "\n")

    print("========== 3. 组合 [values, updates] 模式 ==========")
    for mode, chunk in graph.stream(input_state, stream_mode=["values", "updates"]):
        print(f"  [{mode}]: {chunk}")

    print("\n" + "=" * 60 + "\n")

    print("========== 4. debug 模式 ==========")
    try:
        for chunk in graph.stream(input_state, stream_mode="debug"):
            print(f"  {chunk}")
    except Exception as e:
        print(f"  Debug模式可能需要特殊配置: {e}")


if __name__ == "__main__":
    main()

"""
[输出示例]
=== LangGraph 多模式流式传输演示 ===

========== 1. values 模式 ==========
  {'question': '今天天气怎么样?', 'answer': '', 'confidence': 0.0, 'steps': []}
  {'question': '今天天气怎么样?', 'answer': '', 'confidence': 0.0, 'steps': ['分析问题: 今天天气怎么样?', '检索相关知识', '形成初步答案']}
  {'question': '今天天气怎么样?', 'answer': '今天天气晴朗', 'confidence': 0.9, 'steps': ['分析问题: 今天天气怎么样?', '检索相关知识', '形成初步答案']}
  {'question': '今天天气怎么样?', 'answer': '今天天气晴朗', 'confidence': 0.9, 'steps': ['分析问题: 今天天气怎么样?', '检索相关知识', '形成初步答案', '验证答案: 今天天气晴朗', '置信度评估: 0.9', '结论: 高置信度答案']}

============================================================

========== 2. updates 模式 ==========
  {'think': {'steps': ['分析问题: 今天天气怎么样?', '检索相关知识', '形成初步答案']}}
  {'respond': {'answer': '今天天气晴朗', 'confidence': 0.9}}
  {'reflect': {'steps': ['分析问题: 今天天气怎么样?', '检索相关知识', '形成初步答案', '验证答案: 今天天气晴朗', '置信度评估: 0.9', '结论: 高置信度答案']}}

============================================================

========== 3. 组合 [values, updates] 模式 ==========
  [values]: {'question': '今天天气怎么样?', 'answer': '', 'confidence': 0.0, 'steps': []}
  [updates]: {'think': {'steps': ['分析问题: 今天天气怎么样?', '检索相关知识', '形成初步答案']}}
  [values]: {'question': '今天天气怎么样?', 'answer': '', 'confidence': 0.0, 'steps': ['分析问题: 今天天气怎么样?', '检索相关知识', '形成初步答案']}
  [updates]: {'respond': {'answer': '今天天气晴朗', 'confidence': 0.9}}
  [values]: {'question': '今天天气怎么样?', 'answer': '今天天气晴朗', 'confidence': 0.9, 'steps': ['分析问题: 今天天气怎么样?', '检索相关知识', '形成初步答案']}
  [updates]: {'reflect': {'steps': ['分析问题: 今天天气怎么样?', '检索相关知识', '形成初步答案', '验证答案: 今天天气晴朗', '置信度评估: 0.9', '结论: 高置信度答案']}}
  [values]: {'question': '今天天气怎么样?', 'answer': '今天天气晴朗', 'confidence': 0.9, 'steps': ['分析问题: 今天天气怎么样?', '检索相关知识', '形成初步答案', '验证答案: 今天天气晴朗', '置信度评估: 0.9', '结论: 高置信度答案']}

============================================================

========== 4. debug 模式 ==========
  {'step': 1, 'type': 'task', 'payload': {'name': 'think', ...}}
  {'step': 1, 'type': 'task_result', 'payload': {'name': 'think', 'result': {'steps': ['分析问题: 今天天气怎么样?', '检索相关知识', '形成初步答案']}, ...}}
  {'step': 2, 'type': 'task', 'payload': {'name': 'respond', ...}}
  {'step': 2, 'type': 'task_result', 'payload': {'name': 'respond', 'result': {'answer': '今天天气晴朗', 'confidence': 0.9}, ...}}
  {'step': 3, 'type': 'task', 'payload': {'name': 'reflect', ...}}
  {'step': 3, 'type': 'task_result', 'payload': {'name': 'reflect', 'result': {'steps': [...]}, ...}}
"""
