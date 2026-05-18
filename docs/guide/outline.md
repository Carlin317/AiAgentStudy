---
title: "教程目录大纲"
---

# 教程目录大纲

本大纲为《从入门到精通：AI 智能体实战速成指南》的导航索引，各条目均链接至对应章节的二级标题，便于按知识脉络跳转学习。

---

## 01 大模型基础能力构建

阶段一：会用大模型

### 01-1 大模型（LLM）认识与环境准备

- 大模型的起源与发展历程、大模型与 AGI 关系、AI 应用场景 → [1、认识大模型](/stage1-foundation/ch01-1#1、认识大模型)、[3、大模型如何落地](/stage1-foundation/ch01-1#3、大模型如何落地)
- 国际知名、国产主流大模型的功能特点、优势与适用场景，以及开源 / 闭源差异 → [1.5 大模型的开源 vs 闭源](/stage1-foundation/ch01-1#15-大模型的开源-vs-闭源)
- 大模型分类：按模态（LLM / 多模态理解 / 多模态生成）、按功能（生成式 / 嵌入 / 重排序 / 分类）→ [1.4 大模型分类](/stage1-foundation/ch01-1#14-大模型分类)
- 参数规模与计量单位（B、T、FLOPs）、token 与上下文窗口 → [1.3 大模型计量单位](/stage1-foundation/ch01-1#13-大模型计量单位)
- 训练三阶段：预训练 → 微调 → 推理；预训练、SFT、RLHF/RLAIF 的含义与区别 → [2、大模型是如何"被教会说人话"的？](/stage1-foundation/ch01-1#2、大模型是如何%22被教会说人话%22的%3F)
- 训练与推理的区别、算力从何而来、常见硬件与瓶颈 → [3、大模型如何落地](/stage1-foundation/ch01-1#3、大模型如何落地)

### 01-2 大模型调度平台

- Ollama 定义、安装与本地运行大模型、以及与 LangChain 的整合方式 → [1、Ollama 简介](/stage3-framework/ch12#1、Ollama%20简介)、[2、安装与配置](/stage3-framework/ch12#2、安装与配置)、[4、安装与验证模型](/stage3-framework/ch12#4、安装与验证模型)、[5、LangChain 整合 Ollama](/stage3-framework/ch12#5、langchain-整合-ollama)
- 如何调用私有大模型：在线平台、API 调用、本地客户端 → [4.2 访问大模型的方式](/stage1-foundation/ch01-1#42-访问大模型的方式)
- 云端部署（AWS、阿里云）、本地部署等模型部署流程与方法 → [1、企业级大模型部署概述](/stage2-lowcode/ch07#1、企业级大模型部署概述)、[2、Dify 平台私有化部署](/stage2-lowcode/ch07#2、Dify%20平台私有化部署)、[3、模型部署](/stage2-lowcode/ch07#3、模型部署)

### 01-3 提示词工程

- 提示词工程基础：核心原则、基础结构、基础编写方法 → [1、提示词与提示词工程](/stage1-foundation/ch01-2#1、提示词与提示词工程)、[2、提示词怎么写](/stage1-foundation/ch01-2#2、提示词怎么写)
- 高级技巧：深入上下文控制、任务分解与链式思维提示法、Few-shot 示例与模式引导 → [2.2 核心六要素与典型构成](/stage1-foundation/ch01-2#22-核心六要素与典型构成)、[2.3 Zero-shot 与 Few-shot](/stage1-foundation/ch01-2#23-zero-shot-与-few-shot)
- 多轮对话与结构化组织：System / User / Assistant 消息角色、文件加载提示词 → [2.4 结构化组织方式](/stage1-foundation/ch01-2#24-结构化组织方式)
- 评估提示效果与迭代优化、解决 Prompt 失效与偏差问题 → [3、提示词工程的边界](/stage1-foundation/ch01-2#3、提示词工程的边界)、[4、提示词工程的几个注意点](/stage1-foundation/ch01-2#4、提示词工程的几个注意点)
- 提示词在 Agent 与工具调用中的应用 → [4、智能体开发](/stage1-foundation/ch01-3#4、智能体开发)
- 项目：商品营销卖点提炼、电商 / 自媒体爆款文案生成 → [3.10 商品营销卖点提炼（Coze）](/stage2-lowcode/cases/case-3.10#本案例概要)

### 01-4 大模型架构原理

- 大模型的发展历程、关键推动因素与趋势 → [1.2 为什么会出现大模型？](/stage1-foundation/ch01-1#12-为什么会出现大模型)
- Transformer 编码器 / 解码器结构、可扩展性与 MoE 模型，以及工程实现思路 → [1.2 为什么会出现大模型？](/stage1-foundation/ch01-1#12-为什么会出现大模型)、[4、大模型的工程实现概览](/stage1-foundation/ch01-1#4、大模型的工程实现概览)
- 自注意力机制与多头注意力 → [全书术语表：大模型与训练基础术语](/guide/glossary#3、大模型与训练基础术语)
- LLaMA、Qwen、GPT 等主流体系 → [1.4 大模型分类](/stage1-foundation/ch01-1#14-大模型分类)
- 多模态架构：文本 + 图像 + 音频 + 视频 / 文档 / 图表 / 屏幕 UI 理解 → [1.4 大模型分类](/stage1-foundation/ch01-1#14-大模型分类)

---

## 02 企业低代码平台开发与项目实战

阶段二：低代码做应用

### 02-1 Coze（扣子）平台

- Coze 界面主要功能介绍、主要目标用户 → [4.2 Coze(扣子)介绍](/stage2-lowcode/ch03#_4.2-coze扣子介绍)
- 核心功能模块（插件、知识库、工作流、智能体）的创建与配置 → [4.3 功能说明](/stage2-lowcode/ch03#_4.3-功能说明)
- 提示词设计、模型选择与配置、发布渠道与多端部署能力 → [4、level 3：使用 Coze 搭建高阶智能体](/stage2-lowcode/ch03#_4、level-3使用-coze-搭建高阶智能体)
- Python 调用 Coze 平台工作流 → [1. 发布 API](/stage2-lowcode/ch05#1-发布-api)

### 02-2 项目 1：商户运营管家

- 模块 1：一键生成行业调研 PPT → [3.1 Coze 案例：一键生成行业调研 PPT](/stage2-lowcode/cases/case-3.1#本案例概要)
- 模块 2：复刻爆款视频 → [3.2 Coze 案例：复刻爆款视频](/stage2-lowcode/cases/case-3.2#本案例概要)
- 模块 3：产品营销海报生成 → [3.3 Coze 案例：产品营销海报生成](/stage2-lowcode/cases/case-3.3#本案例概要)
- 模块 4：商品营销卖点提炼 → [3.10 Coze 案例：商品营销卖点提炼](/stage2-lowcode/cases/case-3.10#本案例概要)
- 模块 5：商品评论分析 → [3.8 Coze 案例：商品评论分析](/stage2-lowcode/cases/case-3.8#本案例概要)

### 02-3 Dify AI 平台

- 不同低代码平台对比、Dify 核心功能与组件（工作流、Agent、知识库）→ [5.1 Dify 介绍](/stage2-lowcode/ch03#_5.1-dify-介绍)
- 提示词编排、工具与 Agent、模型集成、工作流基本结构 → [6、工作流的搭建](/stage2-lowcode/ch03#_6、工作流的搭建)
- Dify 案例：客户投诉分类助手 → [3.5 Dify 案例：客户投诉分类助手](/stage2-lowcode/cases/case-3.5#本案例概要)
- Dify 案例：一键生成行业调研报告 → [3.4 Dify 案例：一键生成行业调研报告](/stage2-lowcode/cases/case-3.4#本案例概要)
- Dify 案例：客服对话记录分析 → [3.7 Dify 案例：客服对话记录分析](/stage2-lowcode/cases/case-3.7#本案例概要)
- Dify 案例：商品评论分析 → [3.9 Dify 案例：商品评论分析](/stage2-lowcode/cases/case-3.9#本案例概要)
- Python 调用 Dify 平台工作流 → [1、发布](/stage2-lowcode/ch04#1、发布)

### 02-4 容器化技术

- Docker / Compose 核心概念、镜像、容器、数据卷、端口映射与常用命令 → [第 8 章 Docker 入门与 Dify 部署常见问题](/stage2-lowcode/ch08)
- Docker Desktop 安装与验证 → [第 6 章 2.1 安装 Docker Desktop](/stage2-lowcode/ch06#21-安装-docker-desktop环境准备)
- Dify 部署后的排障、数据位置、备份升级、Navicat 连接与前端自建镜像 → [第 8 章 Docker 入门与 Dify 部署常见问题](/stage2-lowcode/ch08)

### 02-5 企业级大模型部署

- 部署核心方案：应用层（Dify）+ 推理层（Xinference 等）+ OpenAI 兼容 API → [1、企业级大模型部署概述](/stage2-lowcode/ch07#1、企业级大模型部署概述)
- 腾讯云/阿里云服务器部署、Dify 的下载与配置 → [2、Dify 平台私有化部署](/stage2-lowcode/ch07#2、Dify%20平台私有化部署)
- AutoDL 服务器配置、Ollama 下载与大语言模型的加载 → [3、模型部署](/stage2-lowcode/ch07#3、模型部署)
- Xinference 平台下载、嵌入模型与重排序模型的部署 → [3、模型部署](/stage2-lowcode/ch07#3、模型部署)（含 3.2 部署 Xinference、3.4 Embedding、3.5 Rerank）
- 低代码平台 Coze Studio、Dify、Coze Loop 的本地部署 → [1、整体概述](/stage2-lowcode/ch06#1、整体概述)、[3、Coze Studio 的安装和配置](/stage2-lowcode/ch06#3、coze-studio-的安装和配置)、[4、Dify 的安装和启动](/stage2-lowcode/ch06#4、dify-的安装和启动)、[5、Coze Loop（扣子罗盘）指南](/stage2-lowcode/ch06#5、coze-loop扣子罗盘指南)

---

## 03 大模型核心开发框架

阶段三：代码级开发

### 03-1 LangChain 框架原理与应用

- LangChain 框架概述、定位与六大核心模块（Models、Memory、Retrieval、Chains、Agents、Callback）→ [1、LangChain 是什么](/stage3-framework/ch09#1、langchain-是什么)、[3、总体架构与六大核心模块](/stage3-framework/ch09#3、总体架构与六大核心模块)
- LangChain 的安装与调用、环境与依赖 → [3、安装依赖](/stage3-framework/ch10#3、安装依赖)、[4、实战：基于阿里百炼的 HelloWorld](/stage3-framework/ch10#4、实战基于阿里百炼的-helloworld)

**① Model I/O（输入输出与模型接入）**

- Message、Prompt Template、Output Parsers、Function Calling → [1、Model I/O 概述与三件套](/stage3-framework/ch11#1、model-io-概述与三件套)、[1、Prompt 与消息基础](/stage3-framework/ch13#1、prompt-与消息基础)、[1、输出解析器概述](/stage3-framework/ch14#1、输出解析器概述)、[2、Tool 是什么与能干嘛](/stage3-framework/ch17#2、tool-是什么与能干嘛)

**② Chains（链式调用）**

- LCEL 与 Runnable、链式调用（顺序链、分支链、串行链、并行链、函数链）→ [1、Runnable 与统一调用方式](/stage3-framework/ch15#1、runnable-与统一调用方式)、[2、LCEL 是什么](/stage3-framework/ch15#2、lcel-是什么)、[4、链式调用基础用法与案例](/stage3-framework/ch15#4、链式调用基础用法与案例)

**③ Memory（记忆与对话历史）**

- RunnableWithMessageHistory、内存与 Redis 持久化 → [1、为什么需要记忆](/stage3-framework/ch16#_1、为什么需要记忆)、[4、实现原理](/stage3-framework/ch16#_4、实现原理)、[5、实现类介绍：0.3 与 1.0+](/stage3-framework/ch16#_5、实现类介绍%EF%BC%9A0.3%20与%201.0%2B)、[6、案例代码](/stage3-framework/ch16#_6、案例代码)

**④ Agents（智能体与工具调用）**

- Agent 抽象、ReAct 范式、create_agent 与 Executor → [1、Agent 是什么？与 Tool 的关系](/stage3-framework/ch21#1、agent-是什么与-tool-的关系)、[2、演变过程：从多步组装到一步创建](/stage3-framework/ch21#2、演变过程从多步组装到一步创建)、[5、实操与案例](/stage3-framework/ch21#5、实操与案例)
- 现代 Agent 场景：浏览器自动化 / Computer Use、长任务研究代理、代码库维护代理、文件 / 数据分析代理 → [1.4 Agent 的使用场景](/stage3-framework/ch21#14-agent-的使用场景)

**⑤ Retrieval（检索与向量）**

- 文档加载器、Text Splitters、Embedding、向量存储与检索 → [1、向量与向量化](/stage3-framework/ch18#1、向量与向量化)、[2、向量数据库](/stage3-framework/ch18#2、向量数据库)、[2、RAG 文本处理核心知识](/stage3-framework/ch19#2、rag-文本处理核心知识)

- 电商平台商家对话助手案例：集成店铺运营数据库检索、平台政策实时查询和客户服务管理功能；开发多工具调用能力，记忆机制管理多会话上下文；本地知识库的搭建与调用（待更新）

### 03-2 LangGraph 框架原理与应用

- LangGraph 入门：从链式到图状的思维转变 → [1、LangGraph 简介](/stage3-framework/ch22#1、langgraph-简介)、[2、HelloWorld 快速入门](/stage3-framework/ch22#2、helloworld-快速入门)
- 图的核心要素：State、Node、Edge → [1.4 四个核心概念：State、Nodes、Edges、Graph](/stage3-framework/ch22#1.4-四个核心概念：state、nodes、edges、graph)、[2、Graph API 之 State（状态）](/stage3-framework/ch23#2、graph-api-之-state（状态）)、[1、Graph API 之 Node（节点）](/stage3-framework/ch24#1、graph-api-之-node（节点）)、[2、Graph API 之 Edge（边）](/stage3-framework/ch24#2、graph-api-之-edge（边）)
- Graphs：图的构建与编译 → [1、Graph API 之 Graph（图）](/stage3-framework/ch23#1、graph-api-之-graph（图）)、[2.3 Graph 最小构建流程](/stage3-framework/ch22#2.3-graph-最小构建流程)
- Memory：图中的持久化状态与记忆 → [2、状态持久化（Persistence）](/stage3-framework/ch25#2、状态持久化（persistence）)、[3.5 本章和 LangGraph 官方主线的关系](/stage3-framework/ch16#3.5-本章和-langgraph-官方主线的关系)
- Agents：构建更鲁棒、更可控的智能体，覆盖长任务 Agent、多智能体协作与并行任务 → [21-Agent 智能体](/stage3-framework/ch21#1、agent-简介)、[26-LangGraph 多智能体与 A2A](/stage3-framework/ch26#2、supervisor-与-handoff)
- Agent Skills：把可复用提示词、流程、模板、脚本和资源封装成按需加载的能力包 → [27-Skills 技能与 AI 编程工具实践](/stage3-framework/ch27#1、为什么-skills-突然变重要)
- 高级应用与技巧：流式输出（Streaming） → [1、流式处理（Streaming）](/stage3-framework/ch25#1、流式处理（streaming）)

### 03-3 MCP 从原理到实战

- Function Calling 对比 MCP 的核心差异、功能定位、交互逻辑及适用场景 → [4.3 工具调用的实现方式](/stage1-foundation/ch01-3#43-工具调用的实现方式)、[1、为什么需要 MCP](/stage3-framework/ch20#1、为什么需要-mcp)、[2、MCP 是什么（入门概念）](/stage3-framework/ch20#2、MCP%20是什么%EF%BC%88入门概念%EF%BC%89)
- MCP 应用场景、通信机制与传输逻辑（STDIO / SSE），包括浏览器、文件、代码库与数据系统等外部能力接入 → [3、MCP 能做什么](/stage3-framework/ch20#3、mcp-能做什么)、[5、MCP 架构知识](/stage3-framework/ch20#5、mcp-架构知识)
- MCP 关键组成要素，及各要素功能在体系中的作用 → [5.1 主机、客户端、服务器定义](/stage3-framework/ch20#5.1-主机、客户端、服务器定义)、[5.4 FastMCP 的基本写法与常用 API](/stage3-framework/ch20#5.4-fastmcp-的基本写法与常用-api)
- MCP 从初始化到日志记录的完整工作流程，各环节核心动作 → [5.2 MCP 协议层面大致怎么工作](/stage3-framework/ch20#5.2-mcp-协议层面大致怎么工作)、[5.5 完整调用过程理解](/stage3-framework/ch20#5.5-完整调用过程理解)
- 热门 MCP Server 推荐：主流工具，及各工具特点及适用场景 → [4.1 直接使用现成的 MCP 服务](/stage3-framework/ch20#4.1-直接使用现成的-mcp-服务)
- 从底层逻辑剖析 MCP 在服务解耦、路由、容错等方面的核心原理 → [1.2 MCP 到底在解决什么问题](/stage3-framework/ch20#1.2-mcp-到底在解决什么问题)、[5.2 MCP 协议层面大致怎么工作](/stage3-framework/ch20#5.2-mcp-协议层面大致怎么工作)
- 案例：多种具体环境 MCP Server 部署与测试 → [6、案例实战：本地 MCP 天气服务与客户端](/stage3-framework/ch20#6、案例实战本地-mcp-天气服务与客户端)
- 案例：自定义 MCP 的开发步骤、功能验证要点与目标 → [4.2 本地自建 MCP 服务端](/stage3-framework/ch20#4.2-本地自建-mcp-服务端)、[6.2 服务端案例区分理解](/stage3-framework/ch20#6.2-服务端案例区分理解)、[6.4 客户端案例怎么区分理解](/stage3-framework/ch20#6.4-客户端案例怎么区分理解)

### 03-4 跨 Agent 通信：A2A 协议

- A2A 协议定义与作用、与 MCP 协议关系、核心组件架构 → [1、A2A 协议与多智能体架构](/stage3-framework/ch26#1、a2a-协议与多智能体架构)、[1.5 A2A 和 MCP 的区别](/stage3-framework/ch26#1.5-a2a-和-mcp-的区别)
- 工作流程机制、消息格式与数据结构、请求与响应流程 → [1.4 A2A 协议定义](/stage3-framework/ch26#1.4-a2a-协议定义)、[1.6 LangGraph 多智能体和 A2A 是什么关系](/stage3-framework/ch26#1.6-langgraph-多智能体和-a2a-是什么关系)
- 认证与授权机制、错误码与异常处理 → [1、A2A 协议与多智能体架构](/stage3-framework/ch26#1、a2a-协议与多智能体架构)
- 性能优化与并发控制、典型业务场景示例，包括软件工程团队式协作、研究代理团队、数据分析代理团队与并行代码任务 → [1.9 使用场景](/stage3-framework/ch26#1.9-使用场景)、[2.9 Supervisor 和 Handoff 怎么选](/stage3-framework/ch26#2.9-supervisor-和-handoff-怎么选)

---

## 04 企业级 RAG / Agent 项目实战

阶段四：企业级应用

### 04-1 RAG 与知识库基础

- RAG 是什么、为何需要、执行流程（索引阶段 + 检索阶段）→ [1、RAG 的理解](/stage1-foundation/ch02#_1、rag-的理解)、[1、RAG 概述](/stage3-framework/ch19#1、rag-概述)
- 知识库搭建平台对比与选型（Cherry Studio、ima、Dify、RAGFlow 等）→ [2、知识库的概述](/stage1-foundation/ch02#_2、知识库的概述)
- 使用 Cherry Studio、ima、Dify 从零搭建个人/企业知识库 → [3、Cherry-Studio 搭建个人知识库](/stage1-foundation/ch02#_3、cherry-studio-搭建个人知识库)、[4、ima 搭建个人知识库](/stage1-foundation/ch02#_4、ima-搭建个人知识库)、[5、使用 Dify 搭建知识库](/stage1-foundation/ch02#_5、使用-dify-搭建知识库)
- 向量与向量化、向量数据库与 Embedding 实战 → [18-向量数据库与 Embedding 实战](/stage3-framework/ch18#1、向量与向量化)
- RAG 综合案例：文档加载、分割、向量存储、检索与生成 → [3、RAG 综合案例：智能运维助手](/stage3-framework/ch19#3、rag-综合案例智能运维助手)

### 04-2 项目 2：掌柜智库

- 架构设计：基于 LangGraph 构建适配电商设备手册查询、商品售后咨询的可插拔 RAG 工作流（待更新）
- 多模态解析：集成 MinerU 与 OCR，精准解析电商设备操作手册、商品售后指南类图文混排 PDF（待更新）
- 检索机制：采用向量检索 + 稀疏检索 + Neo4j 电商知识图谱（设备故障 - 解决方案关联）多路召回（待更新）
- 智能切片：支持滑动窗口、语义切分策略，适配电商设备故障排查步骤、商品参数说明的语义保留（待更新）
- 深度优化：引入 HyDE 与 BGE-Rerank，提升 “打印机卡纸怎么办”“商品保修政策”等电商疑问匹配精度（待更新）
- 全链路评估：集成 RAGAS 框架，自动化评估电商售后问答准确性、设备操作指引合规性（待更新）

### 04-3 项目 3：智能小二

- 对话理解与意图解析：实现用户模糊咨询的多意图识别，支持上下文关联（如跨轮追问 “之前说的订单退款进度”），精准匹配用户真实需求（待更新）
- 多源知识库联动：对接产品手册、售后工单库、常见问题库（FAQ），实现 “问题 - 答案” 智能映射，支持手册更新后的知识库自动同步与检索优化（待更新）
- 实时交互体验优化：采用流式输出技术减少回复等待时长，配置常见问题快捷回复模板，针对高频咨询（如 “物流查询”）实现 1 秒内响应，支持表情、链接等富文本回复（待更新）
- 人机协同转人工机制：设置转人工触发条件（如复杂投诉、需求不明确），转人工时自动同步当前对话上下文至人工坐席，避免用户重复描述，提升协同效率（待更新）
- 对话数据复盘与优化：自动采集对话日志，分析高频未解决问题、用户满意度低的回复场景，输出优化建议（如补充知识库内容、调整意图识别规则）（待更新）
- 多渠道适配与监控：支持 APP、网页、小程序等多渠道接入，集成服务监控面板，实时查看响应耗时、意图识别准确率、转人工率等核心指标，保障服务稳定性（待更新）

### 04-4 项目 4：电商问数

- 项目定位：自然语言问数把数仓、检索、生成、执行和前端交付串成一条链路 → [3、这个项目到底在做什么](/stage4-projects/ecommerce/#3、这个项目到底在做什么)、[5、这套项目的核心技术栈](/stage4-projects/ecommerce/#5、这套项目的核心技术栈)
- 数仓与元数据基础：先理解事实表、维度表、指标和元数据在问数里的角色 → [3、数据仓库基础](/stage4-projects/ecommerce/ch01#3、数据仓库基础)、[4、维度建模入门](/stage4-projects/ecommerce/ch01#4、维度建模入门)、[2、元数据知识库](/stage4-projects/ecommerce/ch02#2、元数据知识库)
- 工程与基础设施：用 uv、docker-compose、配置管理和客户端封装把 MySQL、Qdrant、Elasticsearch、Embedding 跑起来 → [1、先建立整体认识](/stage4-projects/ecommerce/ch03#1、先建立整体认识)、[1、项目目录结构](/stage4-projects/ecommerce/ch04#1、项目目录结构)、[1、Qdrant 客户端接入](/stage4-projects/ecommerce/ch05#1、qdrant-客户端接入)、[1、Embedding 客户端管理](/stage4-projects/ecommerce/ch06#1、embedding-客户端管理)
- 元数据与检索：围绕表、字段、字段值和指标构建可检索的知识库 → [1、为什么先构建元数据知识库](/stage4-projects/ecommerce/ch07#1、为什么先构建元数据知识库)、[1、本章在整条构建流程中的位置](/stage4-projects/ecommerce/ch08#1、本章在整条构建流程中的位置)、[1、为什么字段检索不能只靠一种能力](/stage4-projects/ecommerce/ch09#1、为什么字段检索不能只靠一种能力)
- 问数工作流：用 LangGraph 组织状态、上下文、关键词抽取、多路召回和上下文合并 → [1、问数智能体的整体工作流](/stage4-projects/ecommerce/ch10#1、问数智能体的整体工作流)、[2、三路召回分别解决什么](/stage4-projects/ecommerce/ch11#2、三路召回分别解决什么)、[2、为什么召回结果不能直接交给大模型](/stage4-projects/ecommerce/ch12#2、为什么召回结果不能直接交给大模型)、[2、为什么合并后还要过滤](/stage4-projects/ecommerce/ch13#2、为什么合并后还要过滤)
- SQL 闭环：完成 SQL 生成、校验、纠错和执行，形成可控的 NL2SQL 流程 → [1、本章在问数链路中的位置](/stage4-projects/ecommerce/ch14#1、本章在问数链路中的位置)、[3、生成 SQL：generate_sql](/stage4-projects/ecommerce/ch14#3、生成-sqlgenerate_sql)、[4、校验 SQL：validate_sql](/stage4-projects/ecommerce/ch14#4、校验-sqlvalidate_sql)、[6、校正 SQL：correct_sql](/stage4-projects/ecommerce/ch14#6、校正-sqlcorrect_sql)、[7、执行 SQL：run_sql](/stage4-projects/ecommerce/ch14#7、执行-sqlrun_sql)
- 接口与联调：用 FastAPI、SSE、QueryService、dependencies 和 lifespan 把能力交给前端并做好排障 → [1、查询接口要解决什么问题](/stage4-projects/ecommerce/ch15#1、查询接口要解决什么问题)、[5、SSE 协议：前后端约定的流式格式](/stage4-projects/ecommerce/ch15#5、sse-协议前后端约定的流式格式)、[3、QueryService：把一次请求变成一次图执行](/stage4-projects/ecommerce/ch16#3、queryservice把一次请求变成一次图执行)、[5、request_id：让并发日志能查得清楚](/stage4-projects/ecommerce/ch17#5、request_id让并发日志能查得清楚)

### 04-5 项目 5：深度研搜

- 项目文档入口与源码仓库：先读 [深度研搜前言](/stage4-projects/deep-research/)，再对照 [deepsearch-agents 源码仓库](https://github.com/didilili/deepsearch-agents) 跑通项目
- DeepAgents 基础：从普通 Agent 过渡到主智能体、子智能体、任务委派和上下文隔离 → [第 1 章 DeepAgents 基础与核心概念](/stage4-projects/deep-research/ch01)、[第 2 章 DeepAgents 快速入门与流式解析](/stage4-projects/deep-research/ch02)、[第 3 章 子智能体进阶与异步执行](/stage4-projects/deep-research/ch03)
- 生态接入与控制能力：把 LangGraph、LangChain、人机协作、Backend、中间件和 Skills 接到 DeepAgents 项目里 → [第 4 章 接入 LangGraph 与 LangChain](/stage4-projects/deep-research/ch04)、[第 5 章 人机协作与中断恢复](/stage4-projects/deep-research/ch05)、[第 6 章 长期记忆与 Backend 存储](/stage4-projects/deep-research/ch06)、[第 7 章 中间件机制与 Skills 配置](/stage4-projects/deep-research/ch07)
- 工程初始化与基础模块：理解项目目录、模型配置、提示词配置、会话目录和上下文变量 → [第 8 章 项目总览与工程初始化](/stage4-projects/deep-research/ch08)、[第 9 章 基础模块与模型配置](/stage4-projects/deep-research/ch09)
- 多来源检索能力：实现网络搜索、MySQL 查询和 RAGFlow 知识库三个子智能体 → [第 10 章 网络搜索子智能体与 Tavily 工具](/stage4-projects/deep-research/ch10)、[第 11 章 数据库查询子智能体与 MySQL 工具](/stage4-projects/deep-research/ch11)、[第 12 章 RAGFlow 子智能体与知识库准备](/stage4-projects/deep-research/ch12)
- 项目闭环：搭建主智能体、异步执行、FastAPI 接口、WebSocket 进度回传和文件交付链路 → [第 13 章 主智能体搭建与异步执行](/stage4-projects/deep-research/ch13)、[第 14 章 FastAPI 接口与项目闭环](/stage4-projects/deep-research/ch14)

---

## 05 大模型微调实践

阶段五：模型定制；面向需要定制领域模型或私有数据的学员

### 05-1 大模型微调核心

- 大模型微调概述、核心要素、数据收集 → [2、微调（Fine-tuning）](/stage1-foundation/ch01-3#2、微调%EF%BC%88Fine-tuning%EF%BC%89)
- 大模型微调数据集处理、Alpaca 指令跟随格式、ShareGPT 多轮对话格式（待更新）
- 大模型微调技术 PEFT 概述、prompt-tuning / p-tuning、zero-shot / few-shot（待更新）
- 大模型量化算法、LoRA 微调、QLoRA 微调（待更新）
- 大模型全参数微调技术详解、DeepSpeed 分布式训练（待更新）
- 大模型训练环境搭建、微调代码详解、微调参数详解（待更新）
- 大模型合并、打包，vLLM 高性能部署（待更新）
- 大模型评估方法与评估指标分析（待更新）

### 05-2 企业级微调数据集构建方法论

- 公开数据集获取、私有数据采集（待更新）
- 标注规范与质量管控（待更新）
- 数据增强技术（待更新）

### 05-3 基于 Llama-Factory 的高效微调

- 环境搭建、参数配置实战（待更新）
- 本地 GPU 单卡/云端多卡训练步骤（待更新）
- 适配部署的 Safetensors/ONNX 格式处理（待更新）

### 05-4 调优案例

- 多个完整调优案例（待更新）

---

## 06 大厂开发规范

### 06-1 企业大模型研发流程

- 流程概述、技术前沿调研、行业实践调研、完整技术调研结构（待更新）
- 自研方案输出、算法框架设计、RAG 项目逻辑、对话系统分发与 pipeline（待更新）
- 评估指标、业务方 / 运营方 / 产品方角色、研发过程、行业趋势与能力培养（待更新）
- 项目立项报告、产品需求、项目设计说明书等（待更新）

### 06-2 大模型当下热点

- Agent/RAG 项目研发主流技术，AI Coding / 代码库级协作、Computer Use / Browser Use、长任务 Agent、多智能体协作等前沿热点跟踪（待更新）

---

## 附录与导航

- **教程案例链接汇总**（在线演示与源码入口）→ [教程案例链接汇总](/guide/case-links)
- **全书术语表**（核心概念速查、易混概念对照）→ [全书术语表](/guide/glossary)
- **新手入门与常见问题**（环境准备、运行案例、API Key 配置、常见报错）→ [新手入门与常见问题](/guide/faq)
- **教程更新日志** → [教程更新日志](/guide/changelog)
