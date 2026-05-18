"""
【案例 12-3】ReAct 模式：推理 + 行动的多步工具调用（产品搜索与库存查询）

知识点速览：
- ReAct（Reason + Act）：先推理，再行动，再根据结果继续推理，是 Agent 最经典的入门机制
- 本案例提供 search_products 和 check_inventory 两个 Tool，Agent 自主决定调用顺序与次数
- 通过 result["messages"] 可追踪完整对话：AIMessage(tool_calls) -> ToolMessage -> 最终 AIMessage
- 使用 create_agent + 本地 @tool 路线；MCP 方式见 11-mcp/McpClientAgent.py
"""

import os

from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langchain_core.tools import tool
from dotenv import load_dotenv

load_dotenv()

# ========== 1. 模拟数据 ==========
PRODUCT_DATABASE = {
    "无线耳机": [
        {"id": "WH-1000XM5", "name": "索尼 WH-1000XM5", "popularity": 95, "price": 299},
        {"id": "QC45", "name": "Bose QuietComfort 45", "popularity": 88, "price": 329},
        {"id": "AIRMAX", "name": "苹果 AirPods Max", "popularity": 92, "price": 549},
        {"id": "PXC550", "name": "森海塞尔 PXC 550", "popularity": 76, "price": 299},
        {"id": "HT450", "name": "JBL Tune 760NC", "popularity": 82, "price": 99},
    ],
    "游戏鼠标": [
        {"id": "GPW", "name": "罗技 G Pro 无线", "popularity": 90, "price": 129},
        {"id": "VIPER", "name": "雷蛇 Viper V2 Pro", "popularity": 87, "price": 149},
        {"id": "DAV3", "name": "雷蛇 DeathAdder V3", "popularity": 85, "price": 119},
    ],
    "笔记本电脑": [
        {"id": "MBP14", "name": "MacBook Pro 14英寸", "popularity": 94, "price": 1999},
        {"id": "XPS13", "name": "戴尔 XPS 13", "popularity": 89, "price": 1299},
        {"id": "TPX1", "name": "ThinkPad X1 Carbon", "popularity": 86, "price": 1499},
    ],
}

INVENTORY_DATABASE = {
    "WH-1000XM5": {"stock": 10, "location": "仓库-A"},
    "QC45": {"stock": 0, "location": "仓库-B"},
    "AIRMAX": {"stock": 5, "location": "仓库-C"},
    "PXC550": {"stock": 15, "location": "仓库-A"},
    "HT450": {"stock": 25, "location": "仓库-B"},
    "GPW": {"stock": 8, "location": "仓库-C"},
    "VIPER": {"stock": 12, "location": "仓库-A"},
    "DAV3": {"stock": 3, "location": "仓库-B"},
    "MBP14": {"stock": 7, "location": "仓库-C"},
    "XPS13": {"stock": 0, "location": "仓库-A"},
    "TPX1": {"stock": 4, "location": "仓库-B"},
}


# ========== 2. 工具定义 ==========
@tool
def search_products(query: str) -> str:
    """搜索产品并返回按受欢迎度排序的结果"""
    print(f"[工具调用] search_products('{query}')")

    keyword_mapping = {
        "无线耳机": ["无线耳机", "蓝牙耳机", "头戴式耳机", "耳机"],
        "游戏鼠标": ["游戏鼠标", "电竞鼠标", "鼠标"],
        "笔记本电脑": ["笔记本电脑", "笔记本", "手提电脑", "电脑"],
    }

    matched_category = None
    for category, keywords in keyword_mapping.items():
        if any(keyword in query for keyword in keywords):
            matched_category = category
            break

    if matched_category and matched_category in PRODUCT_DATABASE:
        products = PRODUCT_DATABASE[matched_category]
        sorted_products = sorted(products, key=lambda x: x["popularity"], reverse=True)
        result = f"找到 {len(sorted_products)} 个匹配 '{query}' 的产品:\n"
        for i, product in enumerate(sorted_products, 1):
            result += f"{i}. {product['name']} (ID: {product['id']}) - 受欢迎度: {product['popularity']}% - {product['price']}元\n"
        return result
    return "未找到匹配产品"


@tool
def check_inventory(product_id: str) -> str:
    """检查特定产品的库存状态"""
    print(f"[工具调用] check_inventory('{product_id}')")

    if product_id in INVENTORY_DATABASE:
        stock_info = INVENTORY_DATABASE[product_id]
        status = "有库存" if stock_info["stock"] > 0 else "缺货"
        return f"产品 {product_id}: {status} ({stock_info['stock']} 件库存) - 位置: {stock_info['location']}"
    return f"未找到产品ID: {product_id}"


# ========== 3. 创建 Agent ==========
model = ChatOpenAI(
    model="qwen-plus",
    api_key=os.getenv("aliQwen-api"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

agent = create_agent(
    model,
    tools=[search_products, check_inventory],
    system_prompt="""你是电商助手，遵循ReAct模式：
    1. 先推理用户需求
    2. 选择合适的工具执行操作
    3. 基于工具结果进行下一步推理
    4. 重复直到获得完整答案

    保持推理步骤简洁明了。""",
)

# ========== 4. 测试 ==========
result = agent.invoke(
    {
        "messages": [
            {"role": "user", "content": "查找当前最受欢迎的无线耳机并检查是否有库存"}
        ]
    }
)

print("\n" + "=" * 40)
print("最终结果:")
for msg in result["messages"]:
    if hasattr(msg, "content"):
        print(f"{msg.__class__.__name__}: {msg.content}")
print("=" * 40)


# ========== 5. 可选：逐条解析 ReAct 循环 ==========
def track_react_cycle(messages):
    print("ReAct 循环步骤分析:")
    step = 1
    for i, msg in enumerate(messages):
        msg_type = msg.__class__.__name__
        if msg_type == "AIMessage" and hasattr(msg, "tool_calls") and msg.tool_calls:
            print(f"\n步骤{step}: Reasoning + Acting")
            for tool_call in msg.tool_calls:
                print(f"  工具调用: {tool_call['name']}({tool_call['args']})")
            step += 1
        elif msg_type == "ToolMessage":
            print(f"  观察结果: {msg.content[:80]}...")
        elif msg_type == "AIMessage" and not (
            hasattr(msg, "tool_calls") and msg.tool_calls
        ):
            print(f"\n最终回答: {msg.content}")


track_react_cycle(result["messages"])
