# AI Job Copilot 里程碑路线图

本文件只记录项目阶段顺序、核心交付和退出条件。

- 当前完成情况和下一次任务：[CURRENT_PROGRESS.md](CURRENT_PROGRESS.md)
- 详细知识、架构和面试参考：[AI_JOB_COPILOT_LEARNING_GUIDE.md](AI_JOB_COPILOT_LEARNING_GUIDE.md)

## 项目主线

```text
Python CLI
→ FastAPI + PostgreSQL
→ LLM 岗位分析
→ 求职资料 RAG
→ RAG 优化与评测
→ 手写 Agent Loop
→ LangGraph Agent
→ 部署与工程化
→ 简历和面试交付
```

日期用于控制节奏，不代替验收。

| 里程碑 | 参考时间 | 目标 |
| --- | --- | --- |
| M1 | 7 月 23 日-7 月 31 日 | 可靠的 Python CLI |
| M2 | 8 月 1 日-8 月 9 日 | FastAPI 多用户后端 |
| M3 | 8 月 10 日-8 月 16 日 | LLM 岗位分析与聊天 |
| M4 | 8 月 17 日-8 月 23 日 | 带引用的 RAG 基础版 |
| M5 | 8 月 24 日-8 月 31 日 | RAG 优化与评测 |
| M6 | 9 月 1 日-9 月 7 日 | 手写安全 Agent Loop |
| M7 | 9 月 8 日-9 月 20 日 | LangGraph 求职 Agent |
| M8 | 9 月 21 日-9 月 30 日 | 部署与工程化 |
| M9 | 10 月 1 日-10 月 15 日 | 简历与面试交付 |

## M1：可靠的 Python CLI

- **核心交付：** 岗位 CRUD、JSON 安全持久化、分层、异常、pytest、Ruff、mypy、coverage、基础 CI 和 asyncio 小练习。
- **退出条件：** 程序与异常路径可靠，核心测试全部通过且覆盖率约 80%，代码检查和 CI 通过，README 可指导安装、运行和测试。

## M2：FastAPI 多用户后端

- **核心交付：** REST API、PostgreSQL、SQLAlchemy、Alembic、JWT，以及岗位、投递时间线、待办和文件管理。
- **退出条件：** 用户数据严格隔离，关键接口覆盖正常、错误、未认证和越权测试，OpenAPI 与 Docker Compose 可完成完整流程。

## M3：LLM 岗位分析与聊天

- **核心交付：** 可替换 LLM Provider、JD 结构化提取、简历匹配、多轮聊天、SSE、校验、重试和成本记录。
- **退出条件：** 非法输出不污染数据库，模型故障可安全处理，上下文和成本可控，业务代码可切换模型配置。

## M4：带引用的 RAG 基础版

- **核心交付：** PDF 解析、清洗、切块、Embedding、pgvector、Metadata Filter、问答和原文引用。
- **退出条件：** 回答可追溯、用户检索隔离、删除文档同步删除向量，并建立至少 20 个问题的初始评测集。

## M5：RAG 优化与评测

- **核心交付：** Query Rewrite、Hybrid Search、Reranker、拒答策略和可重复运行的离线评测。
- **退出条件：** 有真实基线与优化对比，知识库外问题能够拒答，实验配置、效果、延迟和成本可以复现。

## M6：手写安全 Agent Loop

- **核心交付：** 基础 Agent 循环、查询工具、写工具、参数校验、超时、重试、最大步骤、人工确认和审计日志。
- **退出条件：** Agent 不会无限执行，未确认写操作绝不运行，工具失败可安全终止，文档内容不能突破权限。

## M7：LangGraph 求职 Agent

- **核心交付：** 状态图、条件路由、Checkpoint、中断恢复、求职计划、周报和逾期任务调整。
- **退出条件：** 支持拒绝确认和恢复，异常流程有测试，所有写操作可取消、可审计，状态转换可追踪。

## M8：部署与工程化

- **核心交付：** 演示界面、Docker Compose、Redis、后台任务、日志、Trace ID、限流、CI 和在线环境。
- **退出条件：** 新环境可按 README 启动，CI 通过，在线演示、API 文档、架构图、截图和视频齐全，密钥与隐私安全。

## M9：简历与面试交付

- **核心交付：** 简历项目描述、真实量化结果、四种项目介绍，以及 RAG、Agent、Python、后端和大模型原理复盘。
- **退出条件：** 能独立讲清问题、架构、技术选择、评测、安全和局限，并用真实数据证明结果。

## 推进规则

- 当前状态只在 `CURRENT_PROGRESS.md` 维护。
- 详细学习内容只在学习指南维护。
- 一个里程碑未达到退出条件，不进入下一个里程碑。
- 时间不足时优先保证后端、LLM、带引用 RAG、Agent 安全、测试和部署。
- 精致前端、复杂模型路由、OCR、微调、Kubernetes 和多 Agent 可以后置。
