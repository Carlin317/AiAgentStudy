import { defineConfig } from 'vitepress'

export default defineConfig({
  lang: 'zh-CN',
  title: 'AI 智能体实战速成指南',
  description: '从零到企业级落地 — 系统教程 + 可跑源码 + 面试题库 + 企业级实战项目',
  base: '/AiAgentStudy/',

  head: [
    ['link', { rel: 'icon', type: 'image/svg+xml', href: '/AiAgentStudy/logo.svg' }],
  ],

  ignoreDeadLinks: [
    /^https?:\/\/localhost/,
  ],

  markdown: {
    lineNumbers: true,
    math: true,
    image: { lazyLoading: true },
  },

  lastUpdated: true,
  cleanUrls: true,

  themeConfig: {
    siteTitle: 'AI 智能体教程',
    logo: '/images/banner.png',

    nav: [
      { text: '首页', link: '/' },
      { text: '教程大纲', link: '/guide/outline' },
      {
        text: '学习路径',
        items: [
          { text: '阶段 1：大模型基础', link: '/stage1-foundation/ch01-1' },
          { text: '阶段 2：低代码平台', link: '/stage2-lowcode/ch03' },
          { text: '阶段 3：框架开发', link: '/stage3-framework/ch09' },
          { text: '阶段 4：实战项目', link: '/stage4-projects/ecommerce/' },
        ],
      },
      { text: '面试题库', link: '/guide/interview' },
      { text: '术语表', link: '/guide/glossary' },
    ],

    sidebar: {
      '/guide/': [
        {
          text: '参考资料',
          items: [
            { text: '教程目录大纲', link: '/guide/outline' },
            { text: '全书术语表', link: '/guide/glossary' },
            { text: '教程案例链接汇总', link: '/guide/case-links' },
            { text: '新手入门与常见问题', link: '/guide/faq' },
            { text: '工具导航与参考资料索引', link: '/guide/resources' },
            { text: '面试题库', link: '/guide/interview' },
            { text: '更新日志', link: '/guide/changelog' },
            { text: '贡献指南', link: '/guide/contributing' },
          ],
        },
      ],

      '/stage1-foundation/': [
        {
          text: '01 大模型基础能力构建',
          items: [
            { text: '第 1-1 章 大模型认知与工程概览', link: '/stage1-foundation/ch01-1' },
            { text: '第 1-2 章 提示词工程基础', link: '/stage1-foundation/ch01-2' },
            { text: '第 1-3 章 RAG、微调、续训与智能体选型', link: '/stage1-foundation/ch01-3' },
            { text: '第 2 章 RAG 搭建企业私有&个人知识库', link: '/stage1-foundation/ch02' },
          ],
        },
      ],

      '/stage2-lowcode/': [
        {
          text: '02 企业低代码平台开发与项目实战',
          items: [
            { text: '第 3 章 基于 Coze&Dify 的智能体开发', link: '/stage2-lowcode/ch03' },
            {
              text: '智能体的调用与部署',
              collapsed: false,
              items: [
                { text: '第 4 章 Python 调用 Dify 平台工作流', link: '/stage2-lowcode/ch04' },
                { text: '第 5 章 Python 调用 Coze 平台工作流', link: '/stage2-lowcode/ch05' },
                { text: '第 6 章 Coze 与 Dify 的 Windows 平台部署', link: '/stage2-lowcode/ch06' },
                { text: '第 7 章 企业级大模型部署', link: '/stage2-lowcode/ch07' },
                { text: '第 8 章 Docker 入门与 Dify 部署常见问题', link: '/stage2-lowcode/ch08' },
              ],
            },
            {
              text: '工作流智能体案例与源码',
              collapsed: true,
              items: [
                { text: '1 一键生成行业调研 PPT（Coze）', link: '/stage2-lowcode/cases/case-3.1' },
                { text: '2 复刻爆款视频（Coze）', link: '/stage2-lowcode/cases/case-3.2' },
                { text: '3 产品营销海报生成（Coze）', link: '/stage2-lowcode/cases/case-3.3' },
                { text: '4 一键生成行业调研报告（Dify）', link: '/stage2-lowcode/cases/case-3.4' },
                { text: '5 客户投诉分类助手（Dify）', link: '/stage2-lowcode/cases/case-3.5' },
                { text: '6 客服对话记录分析（Coze）', link: '/stage2-lowcode/cases/case-3.6' },
                { text: '7 客服对话记录分析（Dify）', link: '/stage2-lowcode/cases/case-3.7' },
                { text: '8 商品评论分析（Coze）', link: '/stage2-lowcode/cases/case-3.8' },
                { text: '9 商品评论分析（Dify）', link: '/stage2-lowcode/cases/case-3.9' },
                { text: '10 商品营销卖点提炼（Coze）', link: '/stage2-lowcode/cases/case-3.10' },
              ],
            },
          ],
        },
      ],

      '/stage3-framework/': [
        {
          text: '03 大模型核心开发框架',
          items: [
            { text: '第 9 章 LangChain 概述与架构', link: '/stage3-framework/ch09' },
            { text: '第 10 章 LangChain 快速上手与 HelloWorld', link: '/stage3-framework/ch10' },
            { text: '第 11 章 Model I/O 与模型接入', link: '/stage3-framework/ch11' },
            { text: '第 12 章 Ollama 本地部署与调用', link: '/stage3-framework/ch12' },
            { text: '第 13 章 提示词与消息模板', link: '/stage3-framework/ch13' },
            { text: '第 14 章 输出解析器', link: '/stage3-framework/ch14' },
            { text: '第 15 章 LCEL 与链式调用', link: '/stage3-framework/ch15' },
            { text: '第 16 章 记忆与对话历史（含 Redis 基础）', link: '/stage3-framework/ch16' },
            { text: '第 17 章 Tools 工具调用', link: '/stage3-framework/ch17' },
            { text: '第 18 章 向量数据库与 Embedding 实战', link: '/stage3-framework/ch18' },
            { text: '第 19 章 RAG 检索增强生成', link: '/stage3-framework/ch19' },
            { text: '第 20 章 MCP 模型上下文协议', link: '/stage3-framework/ch20' },
            { text: '第 21 章 Agent 智能体', link: '/stage3-framework/ch21' },
            { text: '第 22 章 LangGraph 概述与快速入门', link: '/stage3-framework/ch22' },
            { text: '第 23 章 LangGraph API：图与状态', link: '/stage3-framework/ch23' },
            { text: '第 24 章 LangGraph API：节点、边与进阶', link: '/stage3-framework/ch24' },
            { text: '第 25 章 LangGraph 高级特性', link: '/stage3-framework/ch25' },
            { text: '第 26 章 LangGraph 多智能体与 A2A', link: '/stage3-framework/ch26' },
            { text: '第 27 章 Skills 技能与 AI 编程工具实践', link: '/stage3-framework/ch27' },
          ],
        },
      ],

      '/stage4-projects/': [
        {
          text: '04 企业级项目实战',
          items: [
            {
              text: '电商问数（已完结）',
              collapsed: false,
              items: [
                { text: '前言', link: '/stage4-projects/ecommerce/' },
                { text: '第 1 章 项目概述与数仓基础', link: '/stage4-projects/ecommerce/ch01' },
                { text: '第 2 章 项目整体架构与智能体流程', link: '/stage4-projects/ecommerce/ch02' },
                { text: '第 3 章 开发环境与基础服务准备', link: '/stage4-projects/ecommerce/ch03' },
                { text: '第 4 章 项目结构与基础服务配置管理', link: '/stage4-projects/ecommerce/ch04' },
                { text: '第 5 章 Qdrant 与 ES 快速入门与接入', link: '/stage4-projects/ecommerce/ch05' },
                { text: '第 6 章 MySQL、Embedding 与日志管理', link: '/stage4-projects/ecommerce/ch06' },
                { text: '第 7 章 元数据知识库总览与构建入口', link: '/stage4-projects/ecommerce/ch07' },
                { text: '第 8 章 表与字段信息同步到元数据库', link: '/stage4-projects/ecommerce/ch08' },
                { text: '第 9 章 字段与指标检索能力构建', link: '/stage4-projects/ecommerce/ch09' },
                { text: '第 10 章 问数智能体总览与工作流骨架', link: '/stage4-projects/ecommerce/ch10' },
                { text: '第 11 章 关键词抽取与多路召回', link: '/stage4-projects/ecommerce/ch11' },
                { text: '第 12 章 召回信息合并与上下文构建', link: '/stage4-projects/ecommerce/ch12' },
                { text: '第 13 章 SQL 生成前的信息过滤与补全', link: '/stage4-projects/ecommerce/ch13' },
                { text: '第 14 章 SQL 生成与执行闭环', link: '/stage4-projects/ecommerce/ch14' },
                { text: '第 15 章 API 接口基础与 FastAPI 入门', link: '/stage4-projects/ecommerce/ch15' },
                { text: '第 16 章 查询接口实现与依赖组装', link: '/stage4-projects/ecommerce/ch16' },
                { text: '第 17 章 前后端联调与日志追踪', link: '/stage4-projects/ecommerce/ch17' },
              ],
            },
            {
              text: '深度研搜（已完结）',
              collapsed: false,
              items: [
                { text: '前言', link: '/stage4-projects/deep-research/' },
                { text: '第 1 章 DeepAgents 基础与核心概念', link: '/stage4-projects/deep-research/ch01' },
                { text: '第 2 章 DeepAgents 快速入门与流式解析', link: '/stage4-projects/deep-research/ch02' },
                { text: '第 3 章 子智能体进阶与异步执行', link: '/stage4-projects/deep-research/ch03' },
                { text: '第 4 章 接入 LangGraph 与 LangChain', link: '/stage4-projects/deep-research/ch04' },
                { text: '第 5 章 人机协作与中断恢复', link: '/stage4-projects/deep-research/ch05' },
                { text: '第 6 章 长期记忆与 Backend 存储', link: '/stage4-projects/deep-research/ch06' },
                { text: '第 7 章 中间件机制与 Skills 配置', link: '/stage4-projects/deep-research/ch07' },
                { text: '第 8 章 项目总览与工程初始化', link: '/stage4-projects/deep-research/ch08' },
                { text: '第 9 章 基础模块与模型配置', link: '/stage4-projects/deep-research/ch09' },
                { text: '第 10 章 网络搜索子智能体与 Tavily 工具', link: '/stage4-projects/deep-research/ch10' },
                { text: '第 11 章 数据库查询子智能体与 MySQL 工具', link: '/stage4-projects/deep-research/ch11' },
                { text: '第 12 章 RAGFlow 子智能体与知识库准备', link: '/stage4-projects/deep-research/ch12' },
                { text: '第 13 章 主智能体搭建与异步执行', link: '/stage4-projects/deep-research/ch13' },
                { text: '第 14 章 FastAPI 接口与项目闭环', link: '/stage4-projects/deep-research/ch14' },
              ],
            },
          ],
        },
      ],
    },

    search: {
      provider: 'local',
      options: {
        translations: {
          button: { buttonText: '搜索文档', buttonAriaLabel: '搜索文档' },
          modal: {
            noResultsText: '未找到相关结果',
            resetButtonTitle: '清除查询条件',
            footer: { selectText: '选择', navigateText: '切换', closeText: '关闭' },
          },
        },
      },
    },

    socialLinks: [
      { icon: 'github', link: 'https://github.com/didilili/ai-agents-from-zero' },
    ],

    footer: {
      message: '基于 MIT 许可发布',
      copyright: 'Copyright 2024-2026',
    },

    editLink: {
      pattern: 'https://github.com/Carlin317/AiAgentStudy/edit/main/docs/:path',
      text: '在 GitHub 上编辑此页',
    },

    lastUpdated: {
      text: '最后更新于',
      formatOptions: { dateStyle: 'short', timeStyle: 'short' },
    },

    darkModeSwitchLabel: '主题',
    lightModeSwitchTitle: '切换到浅色模式',
    darkModeSwitchTitle: '切换到深色模式',
    outline: { level: [2, 4], label: '本页目录' },
    docFooter: { prev: '上一页', next: '下一页' },
    returnToTopLabel: '回到顶部',
    sidebarMenuLabel: '菜单',
  },

  sitemap: {
    hostname: 'https://carlin317.github.io/AiAgentStudy/',
  },
})
