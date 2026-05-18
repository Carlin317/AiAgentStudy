"""
【案例 07-5】Redis 环境校验：确认 redis 包已安装且 Redis 服务可连通

对应教程章节：第 16 章 - 记忆与对话历史 → 6、案例代码 → 6.2 持久化：Redis 存储 → 环境验证

知识点速览：
- 使用 RedisChatMessageHistory 前需确认：Python 能导入 redis 包、Redis 服务可达
- 默认检查 redis://localhost:6379；若用 Redis Stack 可设置 REDIS_URL=redis://localhost:26379
- 本脚本不依赖 LangChain，纯粹排查基础环境
"""

import os

try:
    import redis
except ModuleNotFoundError:
    print("未找到 redis 包，请先执行：pip install -r requirements.txt")
    raise SystemExit(1)

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")

print("redis 包导入成功")
print(f"redis 包版本：{redis.__version__}")
print(f"正在连接 Redis：{REDIS_URL}")

client = None
try:
    client = redis.Redis.from_url(REDIS_URL, decode_responses=True)
    print(f"Redis 连接成功，PING -> {client.ping()}")
except (redis.ConnectionError, redis.TimeoutError, redis.ResponseError) as e:
    print("Redis 连接失败")
    print(f"  REDIS_URL = {REDIS_URL}")
    print(f"  错误信息 = {e}")
    print("  如果使用 Redis Stack 的 Docker 端口映射，可尝试：")
    print("  export REDIS_URL=redis://localhost:26379")
    raise SystemExit(1)
except Exception as e:
    print(f"Redis 环境校验异常：{e}")
    raise SystemExit(1)
finally:
    if client is not None:
        client.close()
