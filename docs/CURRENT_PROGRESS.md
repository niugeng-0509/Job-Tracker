# AI Job Copilot 当前进度

本文件记录当前完成情况、验证证据和下一次任务。

最后核对：2026-11-20

## 当前阶段

**M1、M2 已完成并通过验收；下一阶段进入 M3。**

M2 已从单用户 JSON API 演进为 SQLAlchemy 多用户后端。认证、岗位、投递时间线、待办、文件元数据、迁移和 Compose 均已实现，并已在 Docker Desktop 的真实 PostgreSQL 17 环境完成业务与持久化验收。

## M2 已实现

- SQLAlchemy 2 ORM：User、Job、ApplicationEvent、Task、Document
- PostgreSQL URL、psycopg 驱动和 Alembic 初始迁移
- 注册、登录、Argon2 密码哈希、JWT 签发/校验/过期
- 当前用户依赖和 SQLAlchemy 查询条件级 `user_id` 隔离
- 岗位 CRUD、重复检测、分页、排序、状态与关键词筛选
- 投递事件创建与列表
- 待办创建、列表、完成状态筛选和部分更新
- 文件上传、列表、删除、随机存储名、大小和内容检查
- 越权资源统一返回 404，不泄露资源是否存在
- Dockerfile、Compose、`.env.example` 和启动迁移
- OpenAPI 注册、登录、岗位、事件、待办和文件完整路径
- 正式代码集中在 `app/`，M1 完整示例集中在 `examples/m1_cli/`
- M2 路由按 auth、jobs、events、tasks、documents 分类
- Router、Service、Unit of Work、Repository、ORM 五层职责已拆分
- Service 仅依赖 Protocol，SQLAlchemy Repository 由依赖注入层组装
- 领域异常统一映射为 401/404/409/413/415/422/503 响应
- Pydantic Schema 按 auth、jobs、events、tasks、documents 拆分

## 已验证

- `.venv/bin/python -m pytest -q`：58 passed
- `.venv/bin/ruff check .`：All checks passed
- `.venv/bin/python -m mypy app examples`：54 个源码文件无问题
- `.venv/bin/python -m pip check`：无依赖冲突
- 正式后端与 M1 核心层 branch coverage：93.76%，达到 80% 门槛
- Service、Unit of Work 和 SQLAlchemy Repository 分层测试通过
- API 集成测试：认证失败、未认证、岗位 CRUD、分页筛选、404/409/415/422
- 用户隔离测试：跨用户岗位查询、修改、删除、事件和待办均不可访问
- 文件测试：非法 MIME、伪 PDF、文本上传、列表和删除
- Alembic SQLite：upgrade → downgrade → upgrade 通过
- Alembic PostgreSQL offline SQL：UUID、外键、索引和五张表生成通过
- Compose YAML 结构与全部要求的 OpenAPI 路径：程序化验证通过
- Docker Desktop Engine 29.9.3、Compose v5.7.0：镜像构建与容器启动通过
- PostgreSQL 17：健康检查通过，Alembic 自动升级并创建 6 张表
- 真实 HTTP 流程：注册、OAuth2 登录、JWT、岗位、关联任务和文档上传通过
- 真实异常路径：未认证 401、错误密码 401、非法 URL 422
- 容器删除并重建后，岗位、任务、文档元数据和上传文件均保持存在

## M2 验收

- [x] 多用户 REST API、JWT 和密码哈希
- [x] 所有用户资源在 SQL 查询中强制隔离
- [x] 正常、错误、未认证和越权自动测试
- [x] 分页、排序和组合筛选
- [x] Alembic 迁移可升降级并生成 PostgreSQL DDL
- [x] OpenAPI 可覆盖注册、登录、岗位和文件流程
- [x] Dockerfile 与 Compose 配置
- [x] 在 Docker 环境执行 Compose 构建并走通真实 PostgreSQL 与持久化流程

## 下一次最小任务

1. 阅读路线图和学习指南中 M3 的 LLM Provider、提示词和结构化输出章节。
2. 先定义不依赖具体厂商 SDK 的 Provider Protocol 和结构化输出 Schema。
3. 用 Fake Provider 编写首个单元测试，再接入真实模型供应商。

## 已知问题与 Git

- `Job.mark_updated()` 只属于 `examples/m1_cli`；正式 API 使用 ORM 的 `updated_at`。
- `.venv.backup/` 和 `tools/` 已被忽略，不属于项目交付。
- Docker Desktop 已安装；命令行工具当前通过应用内绝对路径调用，未修改全局 shell 配置。
- M1 搬迁、M2 后端、测试、容器和 CI 已提交并推送到 `origin/main`，远程 CI 已通过。
