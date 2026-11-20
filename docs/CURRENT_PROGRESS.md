# AI Job Copilot 当前进度

本文件记录当前完成情况、验证证据和下一次任务。

最后核对：2026-11-20

## 当前阶段

**M1 已完成；M2 功能代码已完成，等待 Docker 环境实机启动验收。**

M2 已从单用户 JSON API 演进为 SQLAlchemy 多用户后端。认证、岗位、投递时间线、待办、文件元数据、迁移和 Compose 均已实现；本机没有 Docker CLI，不能声称 PostgreSQL 容器实际启动通过。

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
- `.venv/bin/python -m mypy app`：41 个源码文件无问题
- `.venv/bin/python -m pip check`：无依赖冲突
- 正式后端与 M1 核心层 branch coverage：93.76%，达到 80% 门槛
- Service、Unit of Work 和 SQLAlchemy Repository 分层测试通过
- API 集成测试：认证失败、未认证、岗位 CRUD、分页筛选、404/409/415/422
- 用户隔离测试：跨用户岗位查询、修改、删除、事件和待办均不可访问
- 文件测试：非法 MIME、伪 PDF、文本上传、列表和删除
- Alembic SQLite：upgrade → downgrade → upgrade 通过
- Alembic PostgreSQL offline SQL：UUID、外键、索引和五张表生成通过
- Compose YAML 结构与全部要求的 OpenAPI 路径：程序化验证通过
- Docker 实际启动：未验证，当前机器没有 `docker` 命令

## M2 验收

- [x] 多用户 REST API、JWT 和密码哈希
- [x] 所有用户资源在 SQL 查询中强制隔离
- [x] 正常、错误、未认证和越权自动测试
- [x] 分页、排序和组合筛选
- [x] Alembic 迁移可升降级并生成 PostgreSQL DDL
- [x] OpenAPI 可覆盖注册、登录、岗位和文件流程
- [x] Dockerfile 与 Compose 配置
- [ ] 在安装 Docker 的环境执行 `docker compose up --build` 并走通真实 PostgreSQL 流程

## 下一次最小任务

1. 在有 Docker 的环境运行 `docker compose up --build`。
2. 从 `/docs` 走通注册、登录、创建岗位和上传文件。
3. 验证通过后将 M2 标记为完全验收，进入 M3 LLM Provider 接口。

## 已知问题与 Git

- `Job.mark_updated()` 只属于 `examples/m1_cli`；正式 API 使用 ORM 的 `updated_at`。
- `.venv.backup/` 和 `tools/` 已被忽略，不属于项目交付。
- M1 搬迁、M2 后端、测试、容器和 CI 已拆分为本地提交，尚未推送；远程 CI 需在 push/PR 后验证。
