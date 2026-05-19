"""
[案例 04-4]模型调用:同步 batch(批量调用)

对应教程章节:第 13 章 - 提示词与消息模板 → 4,调用大模型的调用方式

知识点速览:
- batch 一次处理多条独立输入,返回按顺序一一对应的 AIMessage 列表
- 常见于离线任务,批量评估,数据清洗等场景
- 也可传"消息列表的列表"实现多角色批量调用
"""

import os
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

load_dotenv()

# ========== 1. 实例化模型 ==========
model = init_chat_model(
    model="qwen-plus",
    model_provider="openai",
    api_key=os.getenv("aliQwen-api"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

# ========== 2. 准备批量问题 ==========
questions = [
    "什么是redis?简洁回答,字数控制在100以内",
    "Python的生成器是做什么的?简洁回答,字数控制在100以内",
    "解释一下Docker和Kubernetes的关系?简洁回答,字数控制在100以内",
]

# ========== 3. 批量调用 ==========
response = model.batch(questions)
print(f"响应类型:{type(response)}")
print()

for q, r in zip(questions, response):
    print(f"问题:{q}\n回答:{r.content}\n")

"""
[输出示例]    
响应类型:<class 'list'>
问题:什么是redis?简洁回答,字数控制在100以内
回答:Redis 是一个开源的,基于内存的高性能键值数据库,支持字符串,哈希,列表,集合等多种数据结构,提供持久化,主从复制,事务,发布/订阅等功能,常用于缓存,消息队列,会话存储等场景.

问题:Python的生成器是做什么的?简洁回答,字数控制在100以内
回答:Python生成器是一种惰性迭代器,用`yield`关键字定义,可逐个生成值而非一次性返回全部结果,节省内存.调用时返回生成器对象,支持`next()`或`for`循环遍历,适合处理大数据流或无限序列.

问题:解释一下Docker和Kubernetes的关系?简洁回答,字数控制在100以内
回答:Docker 是容器运行时,负责打包,构建和运行单个容器;Kubernetes(K8s)是容器编排平台,用于自动化部署,扩缩容,调度和管理大规模容器集群.K8s 可以使用 Docker 作为底层容器运行时(现更多用 containerd),但两者职责不同:Docker 关注"如何运行一个容器",K8s 关注"如何管理成百上千个容器".
"""
