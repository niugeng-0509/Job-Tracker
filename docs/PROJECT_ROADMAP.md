# AI Job Tracker 项目路线图

## 1. 项目定位

把当前的命令行求职记录器持续升级为一个可部署的 **AI 求职助手**：

- 管理岗位、投递进度、面试和待办事项
- 保存并检索岗位 JD、简历和面试资料
- 使用 LLM 分析岗位匹配度、提取技能、生成准备建议
- 使用 RAG 基于个人资料和岗位资料回答问题，并返回引用
- 使用 Agent 查询数据、生成周报；涉及写入时要求人工确认

这个项目用一条连续的业务主线覆盖 Python、后端、LLM、RAG、Agent 和工程化，避免做多个只有演示价值的小项目。

## 2. 最终作品应展示的核心能力

| 能力 | 项目中的证明 |
| --- | --- |
| Python 工程基础 | 类型注解、分层设计、异常体系、异步编程、pytest |
| 后端开发 | FastAPI、Pydantic、REST API、JWT、SQLAlchemy、PostgreSQL |
| LLM 应用 | 多轮对话、流式输出、结构化输出、工具调用、重试与成本统计 |
| RAG | 文档解析、切块、Embedding、pgvector、混合检索、重排、引用和拒答 |
| Agent | LangGraph、状态与记忆、工具路由、人工确认、失败重试和执行上限 |
| 工程化 | Redis、后台任务、日志与 Trace ID、限流、Docker、CI/CD、部署 |
| 质量保障 | 单元测试、接口测试、RAG 评测集、性能和成本指标 |

## 3. 推荐技术栈

- Python 3.11+
- FastAPI、Pydantic v2、SQLAlchemy 2、Alembic
- PostgreSQL、pgvector、Redis
- pytest、pytest-asyncio、httpx
- OpenAI-compatible LLM API；在业务层定义统一模型接口，避免绑定单一厂商
- LangGraph（只在理解并实现基础 Agent Loop 后引入）
- React 或轻量前端；前期优先保证后端与 AI 核心链路
- Docker Compose、GitHub Actions

## 4. 数据模型

至少包含以下实体：

- `User`：用户、密码哈希、创建时间
- `Job`：公司、岗位、JD、链接、状态、来源、优先级、截止日期
- `ApplicationEvent`：投递、笔试、面试、Offer 等状态历史
- `Task`：准备任务、截止日期、完成状态
- `Document`：简历、JD、面试资料的文件信息和解析状态
- `Chunk`：文本块、向量、元数据、所属用户和文档
- `Conversation` / `Message`：聊天会话和消息
- `ToolCallLog`：Agent 工具、参数、结果、耗时、错误和确认状态
- `LLMUsage`：模型、Token、延迟和估算成本

所有用户数据都必须带 `user_id`，并在查询层强制隔离。

## 5. 分阶段开发 Backlog

### M1：可靠的 Python CLI（7 月 23 日 - 7 月 31 日）

学习重点：Python、面向对象、类型注解、异常、JSON、pytest、asyncio 概念。

开发任务：

- 使用 `dataclass` 和 `Enum` 定义 `Job`、`JobStatus`
- 将代码拆为 `models`、`services`、`repositories`、`cli`
- 添加公司/岗位非空校验、URL 校验和重复岗位检测
- 支持添加、查看、修改、删除、状态筛选和关键词搜索
- 使用 UUID 作为岗位 ID，不使用列表下标作为业务 ID
- 使用 JSON 持久化，采用临时文件加替换的方式安全写入
- 定义 `ValidationError`、`NotFoundError`、`StorageError`
- 为核心服务和 JSON 仓储编写 pytest
- 独立写一个 asyncio 小练习：并发模拟获取多个 JD

完成标准：

- 退出并重新启动后数据不丢失
- 错误输入不会导致程序退出或数据损坏
- 核心模块测试覆盖率达到 80% 左右
- README 包含安装、运行、测试、功能截图或终端演示

### M2：FastAPI 求职管理后端（8 月 1 日 - 8 月 9 日）

学习重点：REST API、Pydantic、ORM、数据库、认证和接口测试。

开发任务：

- 将 CLI 业务逻辑迁移到 FastAPI，保留 service/repository 分层
- 用户注册、登录、密码哈希、JWT access token
- 岗位 CRUD、分页、排序、状态/公司/关键词筛选
- 投递状态时间线和待办任务 CRUD
- 上传 JD、简历和面试资料，限制类型和大小
- SQLAlchemy 2 + PostgreSQL；使用 Alembic 管理迁移
- 全局异常处理、结构化日志、统一响应和错误码
- OpenAPI 文档和 pytest 接口测试

完成标准：

- 用户只能访问自己的岗位与文件
- 关键接口有正常、参数错误、未认证、越权四类测试
- `docker compose up` 能启动 API 和 PostgreSQL
- API 文档能完成一遍完整业务流程

### M3：LLM 岗位分析与聊天（8 月 10 日 - 8 月 16 日）

学习重点：Prompt、Token、上下文、结构化输出、Function Calling、流式响应。

开发任务：

- 抽象 `LLMProvider`，配置模型、超时、重试和并发限制
- 从 JD 结构化提取：技能、年限、职责、加分项、学历要求
- 对比 JD 与个人技能档案，输出匹配项、差距和准备清单
- 支持针对单个岗位的多轮聊天和 SSE 流式输出
- 保存会话历史，并实现上下文截断或摘要策略
- 添加简单工具：查询岗位详情、查询投递状态
- 记录模型、输入/输出 Token、延迟、错误和估算成本
- 对模型输出使用 Pydantic 校验；失败时修复或安全降级

完成标准：

- 同一接口可以切换至少两个模型配置
- 结构化输出稳定写入数据库，非法输出不会污染数据
- 超时、限流、模型异常有重试和用户可理解的错误信息
- README 解释 temperature、上下文控制和成本权衡

### M4：个人求职知识库 RAG 基础版（8 月 17 日 - 8 月 23 日）

学习重点：解析、切块、Embedding、向量检索、Top-k、Metadata、引用。

开发任务：

- 支持 PDF、Word、TXT；首版先完成 PDF
- 建立“上传 → 解析 → 清洗 → 切块 → Embedding → 入库”流水线
- 比较固定长度切块与按标题/段落切块
- 使用 PostgreSQL + pgvector 保存向量和元数据
- 基于简历、JD、面试笔记回答问题
- 返回文档名、页码/段落、原文片段和相似度
- 用 `user_id`、文档类型、岗位 ID 做 Metadata Filter
- 删除文档时同步删除文本块和向量

完成标准：

- 回答必须带可追溯引用，点击或接口字段能定位原文
- 不同用户之间无法检索到彼此文档
- 为解析、切块、检索分别编写测试
- 用 20 个手工问题建立第一版评测集

### M5：RAG 优化与可量化评测（8 月 24 日 - 8 月 31 日）

学习重点：查询改写、BM25、Hybrid Search、Reranker、拒答与评测。

开发任务：

- PostgreSQL 全文检索/BM25 与向量检索融合
- 添加 Query Rewrite 和可选的多查询检索
- 对候选片段进行 Rerank，再交给 LLM
- 设计相关性阈值和无答案拒答策略
- Redis 缓存会话、热点查询或 Embedding 结果
- 建立离线评测脚本，保存每次实验的配置和结果
- 比较 chunk size、overlap、top-k、reranker 对效果的影响

至少记录：

- Recall@3、Recall@5 或 Top-k 命中率
- 答案正确率、引用正确率、拒答正确率
- P50/P95 响应时间
- 每次请求 Token 与估算成本

完成标准：

- README 展示基线与优化后的对比表，而不只写“效果更好”
- 对知识库没有依据的问题能够明确拒答
- 修改/删除文档后不会检索到过期内容

### M6：基础 Agent Loop（9 月 1 日 - 9 月 7 日）

学习重点：ReAct、状态、记忆、工具路由、人工确认、执行限制。

先不用框架，手写以下循环：

1. 模型判断是否调用工具
2. 校验工具参数
3. 执行只读工具
4. 把结果返回模型
5. 生成最终回复或继续下一步

实现工具：

- 搜索个人知识库
- 查询岗位、投递记录、待办和逾期任务
- 统计本周投递漏斗
- 生成求职周报
- 创建或修改待办（执行前必须人工确认）

安全要求：

- 工具参数使用 Pydantic 校验
- 写工具和只读工具明确分级
- 设置最大步骤、总超时、单工具超时和重试次数
- 每次工具调用记录参数、结果摘要、耗时和错误
- Prompt Injection 场景下，文档内容不能改变系统权限规则

### M7：LangGraph 求职 Agent（9 月 8 日 - 9 月 20 日）

开发任务：

- 把手写 Agent Loop 重构为 LangGraph 状态图
- 设置 planner/router、tool、approval、answer 节点
- 支持断点恢复、会话状态和人工确认
- 完成典型任务：
  - “列出本周需要跟进的岗位并生成行动计划”
  - “根据目标岗位和我的资料生成面试准备清单”
  - “分析本周投递漏斗并生成周报”
  - “为逾期任务调整日期”，确认后才写数据库
- 针对死循环、工具失败、参数错误、用户拒绝确认编写测试

完成标准：

- 任意流程不会无限调用工具
- 所有写操作可审计、可取消
- Agent 的关键状态转换有 Trace ID 和日志

### M8：前端、部署与工程化（9 月 21 日 - 9 月 30 日）

开发任务：

- 做一个简洁前端：岗位看板、文档库、聊天、Agent 确认框、统计页
- Dockerfile + Docker Compose 启动 API、Worker、PostgreSQL/pgvector、Redis
- 大文件解析和 Embedding 改为后台任务
- 环境变量和密钥管理，不把 `.env` 提交到 Git
- 请求日志、Trace ID、健康检查、限流和缓存
- GitHub Actions 执行 lint、type check、test、镜像构建
- 部署一个公开演示环境，准备演示账号和样例数据

完成标准：

- 新环境按 README 可一键启动
- CI 在干净环境通过
- 在线演示、API 文档、架构图、截图和 3-5 分钟视频齐全
- README 明确项目局限、隐私风险和下一步优化方向

### M9：面试材料与原理补齐（10 月 1 日 - 10 月 15 日）

围绕本项目准备：

- 30 秒：项目解决什么问题、核心亮点、结果
- 2 分钟：业务流程、技术栈、本人负责部分
- 5 分钟：架构、RAG 优化、Agent 安全、工程化
- 深挖版：数据库索引、事务、缓存、并发、幂等、限流、检索评测

能够回答：

- 为什么选择 RAG，而不是微调
- chunk size、top-k、reranker 如何用实验确定
- 如何防止幻觉、越权检索和 Prompt Injection
- SSE 流式输出、异步 I/O、后台任务分别解决什么问题
- PostgreSQL/pgvector 的索引和查询如何优化
- Redis 缓存一致性、穿透、击穿和雪崩如何处理
- Agent 为什么需要最大步数、人工确认和审计日志
- Transformer、Attention、Embedding、KV Cache、LoRA、DPO 的基本原理

## 6. 每个功能统一遵循的完成定义

一个功能只有同时满足以下条件才算完成：

- 有清晰的需求或 Issue
- 有类型注解、输入校验和错误处理
- 有正常路径及关键异常路径测试
- 有日志，但不记录密码、Token、完整简历等敏感信息
- 有 API/README 文档
- 代码通过 formatter、lint、type check 和 test
- 能说明为什么这样设计、有什么替代方案和局限

## 7. 优先级与取舍

必须完成：

- Python 工程基础
- FastAPI + PostgreSQL + JWT
- LLM 结构化输出与流式聊天
- 带引用和用户隔离的 RAG
- 有人工确认和执行上限的 Agent
- 测试、Docker、CI、评测数据和 README

时间不足时可后置：

- 精致前端
- 多模型复杂路由
- 多模态/OCR
- 微调训练
- Kubernetes、复杂微服务和大规模分布式架构

项目评价的重点应是：链路完整、结果可测、安全边界清晰、能解释设计，而不是堆叠框架。

## 8. 当前立即开始的任务

建议先创建以下 Issues，并严格按顺序完成：

1. 定义 `Job` dataclass、`JobStatus` enum 和字段校验
2. 实现 JSON repository 与安全写入
3. 实现添加、更新、删除、筛选和搜索 service
4. 重构 CLI，使交互层不直接读写列表
5. 添加自定义异常和统一错误提示
6. 添加 pytest，覆盖模型、repository 和 service
7. 配置 Ruff、mypy、pytest 和基础 CI
8. 更新 README，加入架构、运行、测试和下一阶段计划

完成这 8 项后，再进入 FastAPI，避免把当前全局列表结构直接搬进 Web 项目。
