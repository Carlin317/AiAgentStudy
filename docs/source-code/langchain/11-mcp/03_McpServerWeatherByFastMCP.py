"""
[案例 11-3]用 FastMCP 实现天气查询 MCP 服务(SSE + 指定 host/port)

知识点速览:
- 网络化 MCP Tool 服务:只暴露一个天气查询工具,配合 mcp.json 和 McpClientAgent.py 演示完整链路
- 正确写法:mcp = FastMCP("服务名") -> mcp.run(transport="sse", host=..., port=...)
- 错误写法:FastMCP("服务名", host=..., port=...)  # 构造函数不支持 host/port
- 仓库保留 transport="sse" 用于教学;初学者还需了解 stdio 和 HTTP/Streamable HTTP
"""

from typing import Any

import json
import os

# pip install mcp httpx python-dotenv
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP
import httpx

load_dotenv()

# 构造函数只接受服务名;网络绑定在 run() 时指定
mcp = FastMCP("WeatherServerSSE")


@mcp.tool()
def get_weather(city: str) -> str:
    """查询指定城市的即时天气信息.city 为城市英文名,如 Beijing,Shanghai."""
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": os.getenv("OPENWEATHER_API_KEY"),
        "units": "metric",
        "lang": "zh_cn",
    }
    resp = httpx.get(url, params=params, timeout=10)
    data = resp.json()
    return json.dumps(data, ensure_ascii=False)


if __name__ == "__main__":
    mcp.run(transport="sse", host="127.0.0.1", port=8000)
