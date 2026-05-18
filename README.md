<div align='center'>
  <img src="./docs/images/banner.png" alt="AI 智能体教程" width="950px">
  <h1 style="margin-top: 15px;">AI 智能体实战速成指南（从零到企业级落地）</h1>
  <h4><b>AiAgentStudy</b></h4>
  <p><em>2026 持续更新中 · <b>系统教程 + 可跑源码 + 面试题库 + 企业级实战项目</b>，对齐「AI 智能体 / 大模型应用开发工程师」培训课表与招聘 JD 的一条龙学习路线</em></p>
</div>

<div align="center">

![AI](https://img.shields.io/badge/AI-Agent-00c853?style=flat)
![Language](https://img.shields.io/badge/language-Chinese-2ea44f?style=flat)
![Stars](https://img.shields.io/github/stars/Carlin317/AiAgentStudy?logo=github&style=flat)
[![GitHub](https://img.shields.io/badge/GitHub-Project-181717?logo=github&logoColor=white)](https://github.com/Carlin317/AiAgentStudy)

[快速开始](#quick-start) · [教程大纲](docs/guide/outline.md) · [案例汇总](docs/guide/case-links.md) · [更新日志](docs/guide/changelog.md) · [面试题库](docs/guide/interview.md) · [新手入门与常见问题](docs/guide/faq.md)

</div>

**更新说明**：教程持续迭代中，为 **2026 年最新版 AI 智能体** 笔记与教程，预计 5 月第一版更新完毕，完成「从入门到企业级」闭环。

概念篇已全部更新完毕，两个完整实战项目也已更新完毕：`NL2SQL + LangGraph` 实战项目 [电商问数](docs/stage4-projects/ecommerce/index.md)（[源码仓库](https://github.com/Carlin317/shopkeeper-agent)）已于 5 月 3 日完成。`DeepAgents` 多智能体实战项目 [深度研搜](docs/stage4-projects/deep-research/index.md)（[源码仓库](https://github.com/Carlin317/deepsearch-agents)）已于 5 月 17 日完成。你可以点击[更新日志](docs/guide/changelog.md)了解最新仓库动态。若对你有帮助，欢迎 Star。

---

## 教程亮点

- **系统性学习路径**：从大模型与提示词，到低代码（Coze/Dify）与代码框架（LangChain/LangGraph），再到企业级 RAG/Agent、微调与工程规范——按知识体系统一编排，完整链路闭环，适合系统学习而不是碎片化收藏。
- **聚焦 Python 生态**：主线只讲 **Python**，重点是 **LangChain / LangGraph** 这条路线，不走 Spring AI / langchain4j 的 Java 路线。
- **通俗易懂，适合零基础**：由浅入深编排，先讲清大模型、提示词、Agent、RAG、MCP 等核心概念，再逐步进入框架与项目实战，适合第一次系统学习大模型智能体开发的人。
- **企业级实战**：以商户运营管家、电商问数、深度研搜、掌柜智库、智能小二、市场罗盘等为主线，串起意图解析、多源知识、转人工、复盘与监控；把多路召回、评测、观测、成本、护栏放进真实语境里练。写简历、讲项目有抓手。
- **每个案例都能跑起来**：提供可运行案例、源码、环境说明和常见问题排查，帮助你少踩坑、尽快上手。
- **教程 + 源码 + 面试三位一体**：可运行案例与源码、提示词模板与部署思路。面试题库按培训班与 JD 常见能力域拆题，部分题目整理自大厂真实面试题和高频追问场景，适合转岗/应届集中复盘。
- **面向 2026，持续更新**：技术栈与问法随生态迭代，对齐「AI 应用开发工程师」培训课表维度，额外覆盖高频面试答法。

---

## 技术栈概览

| 类别             | 技术/平台                                     | 说明                                                                                     |
| ---------------- | --------------------------------------------- | ---------------------------------------------------------------------------------------- |
| **大模型与基础** | LLM、Transformer、MoE、自注意力               | LLaMA/Qwen/GPT、多模态、预训练/微调/推理                                                 |
| **提示与编排**   | 提示词工程、Chain of Thought、Few-shot        | 多轮对话、记忆管理、Agent 与工具调用                                                     |
| **低代码平台**   | Coze（扣子）、Dify                            | 工作流、Agent、知识库、插件、Python 调用                                                 |
| **开发框架**     | LangChain、LangGraph                          | Model I/O、Chains、Memory、Agents（ReAct）、Retrieval、图状工作流                        |
| **协议与通信**   | MCP（Model Context Protocol）、A2A            | Function Calling、服务解耦、跨 Agent 通信                                                |
| **RAG 与检索**   | 向量数据库、稀疏检索、Neo4j、HyDE、BGE-Rerank | 多路召回、知识图谱、RAGAS 评估                                                           |
| **文档与多模态** | MinerU、OCR                                   | 图文混排 PDF 解析、设备手册与售后指南                                                    |
| **部署与运维**   | Docker、Ollama、Xinference、vLLM              | 腾讯云/阿里云、AutoDL、Coze 本地部署                                                     |
| **微调与训练**   | PEFT、LoRA、QLoRA、DeepSpeed、Llama-Factory   | Alpaca/ShareGPT 数据格式、Safetensors/ONNX                                               |
| **编程与工具**   | Python；Trae AI、Qoder（辅助 IDE）            | 主语言为 Python；Trae / Qoder 为教程中涉及的 AI 编程辅助工具，多模型 API、MCP 接入与调试 |
| **求职与面试**   | 面试题库                                      | 按岗位能力域组织 **问法 + 答法**；对齐同类**线上培训结业能力**与 **JD** 高频考点         |

---

## 你学完能收获什么？

- **可上线的项目能力**，能独立交付 AI Agent 应用（从环境到部署），从「只会调 API」进阶到能落地的工程实践。
- **体系化的架构表达**，能讲清楚 RAG、Agent、MCP 等设计与取舍，面试与简历里经得起追问。
- **面试与 JD 对齐**，独立 [面试题库](docs/guide/interview.md)，与正文题号互链，按岗位能力域组织问法与答法，适合应届与转岗梳理口径。
- **工程化与简历素材**，企业向案例与多路召回、观测、成本等表述，项目可演示、可写进简历。
- **可检索的知识地图**，成体系目录 + 案例源码，与常见「智能体 / 应用开发」课表维度对齐，便于对照补缺，少踩「只看过文章没跑过」的坑。
- **明确的岗位对标**，可胜任 AI 应用开发工程师、AI Agent 工程师、AI 自动化流程开发及 AI 产品技术负责人等方向；尤其适合前端 / 后端 / 产品等背景转型 AI 与智能体开发。

---

## 教程大纲（节选）

完整导航见 **[教程目录大纲](docs/guide/outline.md)**。

### 01 大模型基础能力构建

| 章节名称                    | 内容概要                                                                         |
| --------------------------- | -------------------------------------------------------------------------------- |
| 大模型（LLM）认识与环境准备 | 起源与发展、AGI 关系、主流模型特点与适用场景、预训练/微调/推理                   |
| 大模型架构原理              | Transformer、MoE、自注意力、LLaMA/Qwen/GPT、多模态                               |
| 大模型调度平台              | Ollama、私有大模型调用、云端/本地部署（AWS、阿里云等）                           |
| 提示词工程                  | 核心原则与结构、链式思维与 Few-shot、多轮对话与记忆、在 Agent 与工具调用中的应用 |

### 02 企业低代码平台开发与项目实战

| 章节名称                  | 内容概要                                                                           |
| ------------------------- | ---------------------------------------------------------------------------------- |
| Coze（扣子）平台          | 界面与功能、插件/知识库/工作流/智能体、Python 调用工作流                           |
| 项目 1：商户运营管家      | 行业调研 PPT、爆款视频复刻、营销海报、卖点提炼、评论分析                           |
| Dify AI 平台              | 工作流/Agent/知识库、多案例（投诉分类、调研报告、客服分析、评论分析）、Python 调用 |
| 容器化技术                | Docker 核心概念、安装与常用命令                                                    |
| 企业级大模型部署          | 腾讯云/阿里云、Docker、Dify、AutoDL、Ollama、Xinference、Coze 本地部署             |
| AI 代码编程工具 - Trae AI | 安装使用、多模型 API、MCP 接入                                                     |
| AI 代码编程工具 - Qoder   | 使用与调试、项目开发                                                               |

### 03 大模型核心开发框架

| 章节名称                 | 内容概要                                                                    |
| ------------------------ | --------------------------------------------------------------------------- |
| LangChain 框架原理与应用 | Model I/O、Chains、Memory、Agents（ReAct）、Retrieval、电商商家对话助手案例 |
| LangGraph 框架原理与应用 | 图状思维、State/Node/Edge、持久化记忆、流式输出                             |
| MCP 从原理到实战         | 与 Function Calling 对比、通信机制、工作流程、Server 部署与自定义开发       |
| 跨 Agent 通信：A2A 协议  | 与 MCP 关系、消息与认证、典型场景                                           |

### 04 企业级 RAG / Agent 项目实战

| 章节名称                                | 内容概要                                                                                                                                                                               |
| --------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 掌柜智库                                | LangGraph RAG 工作流、MinerU/OCR、向量+稀疏+Neo4j 多路召回、HyDE/BGE-Rerank、RAGAS 评估                                                                                                |
| 智能小二                                | 意图解析、多源知识库、流式回复、转人工机制、对话复盘、多渠道与监控                                                                                                                     |
| [电商问数](docs/stage4-projects/ecommerce/index.md) | 围绕自然语言问数，完整串起 MySQL 数仓、元数据知识库、Qdrant 向量检索、Elasticsearch 字段值检索、LangGraph 工作流、SQL 生成校验执行、FastAPI SSE 和前后端联调                           |
| [深度研搜](docs/stage4-projects/deep-research/index.md) | 基于 [DeepAgents](docs/stage4-projects/deep-research/ch01.md) 搭建多智能体研究系统，串起网络搜索、MySQL 查询、RAGFlow 知识库、文件读取生成、FastAPI 接口和 WebSocket 实时进度回传 |
| 市场罗盘                                | 场景化任务拆解、从 0 到 1 设计与开发、阶段目标与进度管控、代码评审与成果展示                                                                                                           |

> **已完成实战项目推荐：**
>
> - [电商问数](docs/stage4-projects/ecommerce/index.md)（[源码仓库](https://github.com/Carlin317/shopkeeper-agent)）：不是简单的 SQL 生成 Demo，而是把 `MySQL`、`LangGraph`、`Qdrant`、`Elasticsearch`、`FastAPI` 等知识点放进同一条可运行的智能问数链路里。
> - [深度研搜](docs/stage4-projects/deep-research/index.md)（[源码仓库](https://github.com/Carlin317/deepsearch-agents)）：不是普通聊天框，而是围绕开放研究任务，把主智能体调度、子智能体分工、多来源资料检索、文件生成交付和前后端实时联动做成一条完整闭环。

### 05 大模型微调实践

| 章节名称                      | 内容概要                                                                                 |
| ----------------------------- | ---------------------------------------------------------------------------------------- |
| 大模型微调核心                | 数据与格式（Alpaca、ShareGPT）、PEFT/LoRA/QLoRA、全参数微调与 DeepSpeed、vLLM 部署、评估 |
| 企业级微调数据集构建          | 公开/私有数据、标注与质量、数据增强                                                      |
| 基于 Llama-Factory 的高效微调 | 环境与参数、单卡/多卡、Safetensors/ONNX                                                  |
| 调优案例                      | 学习率与 LoRA 秩、loss/评测对比、业务场景下的迭代策略；多组对照的完整微调—评测—部署案例  |

### 06 大厂开发规范

| 章节名称           | 内容概要                                                              |
| ------------------ | --------------------------------------------------------------------- |
| 企业大模型研发流程 | 技术调研、方案与框架设计、RAG 与 pipeline、评估与角色、立项与需求文档 |
| 大模型当下热点     | Agent/RAG 主流技术、前沿与热点跟踪                                    |

---

## Agent 项目架构与技术架构

![智能体生态架构图](docs/images/智能体生态架构图.png)

---

<a id="quick-start"></a>

## 快速开始

想马上跑通一个案例？按下面几步即可。更详细的环境说明、API 申请、常见报错处理见 [新手入门与常见问题](docs/guide/faq.md)。

1. **克隆仓库并进入项目目录**

   ```bash
   git clone https://github.com/Carlin317/AiAgentStudy.git
   cd AiAgentStudy
   ```

2. **准备环境**（推荐 Python 3.10，支持 3.10–3.13）

   ```bash
   python3.10 -m venv .venv
   source .venv/bin/activate          # macOS/Linux
   # .venv\Scripts\activate           # Windows CMD
   pip install -r requirements.txt
   ```

3. **配置 API Key**
   - 将根目录下的 `.env-example` 复制为 `.env`
   - 在 `.env` 中填入你的 API Key（如通义千问/阿里百炼、DeepSeek 等），变量名需与代码一致（如 `aliQwen-api`、`QWEN_API_KEY`、`deepseek-api`）
   - 各平台 Key 的申请方式见 [新手入门与常见问题](docs/guide/faq.md)

4. **在项目根目录运行第一个案例**

   ```bash
   python docs/source-code/langchain/01-helloworld/05_StandardDesc.py
   ```

   **注意**：必须在**项目根目录**执行 `python`，否则会读不到 `.env`。若不想用云 API，可使用 Ollama 本地模型（无需 Key），详见 [新手入门与常见问题](docs/guide/faq.md)。

遇到 `ModuleNotFoundError`、API Key 报错、找不到 `.env` 等，请查看 [新手入门与常见问题](docs/guide/faq.md)。

---

## 关于本仓库

- **目标**：做一套**真正适合入门的智能体速成教程**，不仅能把概念讲清楚，还能把案例跑起来，让你从 0 到能独立做 **RAG / Agent** 类项目，并能用工程化语言讲清楚自己的方案与项目。
- **技术定位**：聚焦 **Python 智能体开发路线**，重点讲 **LangChain / LangGraph** 及相关工程实践，**不走 Spring AI / langchain4j 的 Java 路线**，更适合想直接进入 Python 大模型应用开发的同学。
- **教程来源**：参考尚硅谷《大模型智能体线上速成班》等课程资料，并在此基础上结合公开文档、社区实践与项目经验持续**重构、补充与维护**，逐步整理成一套 **Python 智能体应用开发** 的系统化学习资料。
- **面试题来源**：题库中有相当一部分题目整理自**大厂真实面试题**、公开面经与高频追问场景，并结合本仓库的章节主线做了工程化重构，更适合按项目和系统设计视角复习。
- **内容构成**：**系统章节笔记** + **可运行案例源码** + **[面试题库](docs/guide/interview.md)** （对标同类线上培训与社招/校招 JD）。

---

## ⭐ Star History

[![Star History Chart](https://api.star-history.com/svg?repos=Carlin317/AiAgentStudy&type=Date)](https://star-history.com/#Carlin317/AiAgentStudy&Date)

---

**仓库名**：`AiAgentStudy` · **中文名**：《AI 智能体实战速成指南：从零到企业级落地》
