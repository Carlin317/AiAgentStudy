"""
[案例 12-4]Agent-to-Agent(A2A)协作:携程订机票 + 美团订酒店 + 滴滴打车

知识点速览:
- A2A = 多个专属 Agent 各司其职 + 一个总协调逻辑负责调度与汇总
- 子 Agent 实现方式:Prompt | llm.bind_tools([单工具]) | output_parser,单一职责
- 总协调使用 RunnableLambda 封装按顺序调度 + 失败兜底的编排逻辑
- 子 Agent 统一 invoke({"input": "..."}) 接口;@tool 的 description 写清参数便于模型传参
"""

import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda
from langchain_core.tools import tool
from dotenv import load_dotenv

load_dotenv()


# ========== 1. 大模型与输出解析 ==========
llm = ChatOpenAI(
    model="qwen-plus",
    api_key=os.getenv("aliQwen-api"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)
output_parser = StrOutputParser()


# ========== 2. 模拟业务工具 ==========
@tool(
    "CtripBookFlight",
    description="预订机票的唯一工具,必须调用,参数是departure出发地,arrival目的地,date出行日期(格式2026-02-01)",
)
def ctrip_book_flight(departure: str, arrival: str, date: str) -> str:
    """携程订机票"""
    return f"[携程机票预订成功]\n出发地:{departure}\n目的地:{arrival}\n出行日期:{date}\n航班号:CA1885(北京首都T3->上海浦东T2)\n起飞时间:14:00\n降落时间:16:30\n座位:经济舱34A\n电子客票号:999-1234567890\n舱位等级:经济舱超级经济座"


@tool(
    "MeituanBookHotel",
    description="预订酒店的唯一工具,必须调用,参数是city城市,near_by附近地标,check_in入住日期,check_out离店日期",
)
def meituan_book_hotel(city: str, near_by: str, check_in: str, check_out: str) -> str:
    """美团订酒店"""
    return f"[美团酒店预订成功]\n城市:{city}\n位置:{near_by}附近\n入住日期:{check_in}\n离店日期:{check_out}\n酒店名称:上海浦东机场铂尔曼大酒店\n房型:豪华大床房(含双人自助早餐)\n房号:1508\n预订号:MT20260201001\n入住人:张三\n退房政策:入住后24小时内可免费取消"


@tool(
    "DidiBookTaxi",
    description="预约打车的唯一工具,必须调用,参数是start起点,end终点,time用车时间",
)
def didi_book_taxi(start: str, end: str, time: str) -> str:
    """滴滴打车"""
    return f"[滴滴打车预约成功]\n起点:{start}\n终点:{end}\n用车时间:{time}\n车型:滴滴快车(舒适型)\n司机姓名:王师傅\n车牌号:沪A12345\n司机电话:13800138000\n预估费用:35元(券后立减5元,实付30元)\n预计接驾时间:16:35\n车型空间:5座,可放2件24寸行李箱"


# ========== 3. 专属 Agent:每条子链只绑定一个工具 ==========
def create_ctrip_agent(llm):
    llm_with_tools = llm.bind_tools([ctrip_book_flight])
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "你是专业的工具调用助手,只能调用CtripBookFlight工具,"
                "调用格式必须正确,"
                "直接传入参数:departure='北京', arrival='上海', date='2026-02-01',"
                "调用后直接返回工具执行的完整字符串结果,不能有任何其他内容,不能留空!",
            ),
            ("human", "{input}"),
        ]
    )
    return prompt | llm_with_tools | output_parser


def create_meituan_agent(llm):
    llm_with_tools = llm.bind_tools([meituan_book_hotel])
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "你是专业的工具调用助手,只能调用MeituanBookHotel工具,调用格式必须正确,"
                "直接传入参数:city='上海', near_by='浦东机场', check_in='2026-02-01', "
                "check_out='2026-02-02',调用后直接返回工具执行的完整字符串结果,"
                "不能有任何其他内容,不能留空!",
            ),
            ("human", "{input}"),
        ]
    )
    return prompt | llm_with_tools | output_parser


def create_didi_agent(llm):
    llm_with_tools = llm.bind_tools([didi_book_taxi])
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "你是专业的工具调用助手,只能调用DidiBookTaxi工具,调用格式必须正确,"
                "直接传入参数:start='上海浦东机场T2', end='上海浦东机场铂尔曼大酒店', "
                "time='2026-02-01 16:40',调用后直接返回工具执行的完整字符串结果,"
                "不能有任何其他内容,不能留空!",
            ),
            ("human", "{input}"),
        ]
    )
    return prompt | llm_with_tools | output_parser


# ========== 4. 总协调器 ==========
def create_travel_coordinator_agent(llm, ctrip_chain, meituan_chain, didi_chain):
    """按业务顺序调用子链,必要时用 .func 兜底."""

    def a2a_schedule(input_dict):
        print("开始执行 A2A 协作,依次调用各业务 Agent...\n")
        ctrip_func = ctrip_book_flight.func
        meituan_func = meituan_book_hotel.func
        didi_func = didi_book_taxi.func

        # 4.1 携程 Agent
        print("1. 调用[携程机票 Agent]>>>")
        try:
            ctrip_result = ctrip_chain.invoke({"input": "订机票"})
        except Exception:
            ctrip_result = ""
        if not ctrip_result.strip():
            ctrip_result = ctrip_func("北京", "上海", "2026-02-01")
        print(f"携程结果:\n{ctrip_result}\n" + "-" * 80 + "\n")

        # 4.2 美团 Agent
        print("2. 调用[美团酒店 Agent]>>>")
        try:
            meituan_result = meituan_chain.invoke({"input": "订酒店"})
        except Exception:
            meituan_result = ""
        if not meituan_result.strip():
            meituan_result = meituan_func(
                "上海", "浦东机场", "2026-02-01", "2026-02-02"
            )
        print(f"美团结果:\n{meituan_result}\n" + "-" * 80 + "\n")

        # 4.3 滴滴 Agent
        print("3. 调用[滴滴打车 Agent]>>>")
        try:
            didi_result = didi_chain.invoke({"input": "预约打车"})
        except Exception:
            didi_result = ""
        if not didi_result.strip():
            didi_result = didi_func(
                "上海浦东机场T2", "上海浦东机场铂尔曼大酒店", "2026-02-01 16:40"
            )
        print(f"滴滴结果:\n{didi_result}\n" + "-" * 80 + "\n")

        # 整合报告
        total_report = f"""
[携程-美团-滴滴 A2A 协作报告]
{'=' * 80}
协作流程:携程订机票 -> 美团订酒店 -> 滴滴打车

[1. 携程机票预订结果]
{ctrip_result}

[2. 美团酒店预订结果]
{meituan_result}

[3. 滴滴打车预约结果]
{didi_result}
{'=' * 80}
"""
        return total_report

    return RunnableLambda(a2a_schedule)


# ========== 5. 主程序 ==========
if __name__ == "__main__":
    try:
        print("初始化携程/美团/滴滴专属 Agent...")
        ctrip_chain = create_ctrip_agent(llm)
        meituan_chain = create_meituan_agent(llm)
        didi_chain = create_didi_agent(llm)
        print("所有 Agent 初始化完成\n" + "=" * 80 + "\n")

        print("初始化 A2A 总协调 Agent...")
        coor_chain = create_travel_coordinator_agent(
            llm, ctrip_chain, meituan_chain, didi_chain
        )
        print("总协调 Agent 初始化完成\n" + "=" * 80 + "\n")

        print("A2A 协作测试开始")
        final_result = coor_chain.invoke(
            {"input": "安排2026-02-01北京飞上海的完整行程"}
        )

        print("\n" + "=" * 80)
        print(final_result)
        print("=" * 80)

    except Exception as e:
        print(f"运行异常:{type(e).__name__} - {str(e)[:100]}")
        print(
            "排查:1. 通义密钥是否正确 2. 网络能否访问阿里云 3. LangChain 版本"
        )
