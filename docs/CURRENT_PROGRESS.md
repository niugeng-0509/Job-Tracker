# AI Job Copilot 当前进度

本文件记录当前完成情况、验证证据和下一次任务。

最后核对：2026-08-02

## 当前阶段

**M1 已完成，M2 进行中：最小 FastAPI 应用已建立**

可靠 Python CLI 已通过 M1 验收。M2 已完成独立 FastAPI 应用入口、`GET /health`、接口测试和依赖记录；岗位 Schema、CRUD API、数据库与认证尚未开始。

## M1 已完成

- `Job` dataclass、`JobStatus` enum、UUID、时间字段和输入校验
- Model、Repository、Service、CLI 分层及构造函数依赖注入
- 岗位 CRUD、状态筛选、关键词搜索和重复岗位检测
- JSON 往返和永久保存，临时文件、`fsync`、`os.replace` 安全写入
- `ValidationError`、`JobNotFoundError`、`StorageError` 和 CLI 友好提示
- Model、Service、JSON Repository 的正常与关键异常路径测试
- Fake Repository、pytest fixture、`tmp_path` 和真实数据隔离
- `pyproject.toml` 中的 pytest、Ruff、mypy 和 coverage 配置
- 业务层 80% coverage 门槛、Ruff 和 mypy 严格检查
- GitHub Actions 在 push/PR 时自动执行质量检查
- asyncio JD 练习：顺序执行、`gather()` 并发、异常校验和 4 个测试
- README 架构、数据流、安装、运行、测试、asyncio 和 CI 说明
- 项目路线图和完整学习架构指南

## 已验证

- `.venv/bin/python -m compileall -q app examples`：通过
- `.venv/bin/python -m pytest -q`：40 passed
- `.venv/bin/python -m pytest --cov=app.models --cov=app.services --cov=app.repositories --cov-report=term-missing --cov-fail-under=80`：40 passed
- 业务逻辑 branch coverage：91.50%，达到 80% 门槛
- `.venv/bin/ruff check .`：All checks passed
- `.venv/bin/python -m mypy app examples`：15 个源码文件无问题
- `.venv/bin/python -m pip check`：无依赖冲突
- CLI 输入 `7`：菜单正常显示并退出
- Uvicorn 实际启动：`GET /health` 返回 200 和 `{"status":"ok"}`，`POST /health` 返回 405
- `/docs` 返回 200，OpenAPI 包含 `GET /health`
- `.venv/bin/python -m examples.async_jd_fetch`：顺序约 0.90 秒，并发约 0.30 秒
- GitHub Actions run `30730553236`：提交 `eaecb34` 状态 `completed / success`

coverage 只统计 Model、Service 和 Repository；CLI、API、`main.py` 和 asyncio 示例不计入 91.50%。`/health` 有 2 个独立接口测试。M2 的 CI 已从 `requirements-dev.txt` 安装依赖，并在远程运行成功。

## M1 验收

- [x] CLI 正常路径和关键异常路径可靠
- [x] JSON 安全持久化，不覆盖损坏文件
- [x] 测试不操作真实 `data/jobs.json`
- [x] 业务逻辑 coverage 超过 80%
- [x] Ruff、mypy 和 pytest 通过
- [x] 基础 GitHub Actions CI 通过
- [x] 独立 asyncio 并发练习通过
- [x] README 可指导安装、运行和测试

## M2 进度

- [x] 独立 FastAPI 应用骨架和 `GET /health`
- [x] 健康检查正常路径、错误方法测试和 OpenAPI 验证
- [x] 运行与开发依赖文件，CI 改为从依赖文件安装
- [ ] 岗位请求/响应 Pydantic 模型和 CRUD API
- [ ] PostgreSQL、SQLAlchemy 2 和 Alembic
- [ ] 注册、登录、密码哈希和 JWT
- [ ] 用户岗位、时间线、待办和文件的数据隔离
- [ ] 分页、排序、筛选及正常/错误/未认证/越权测试
- [ ] OpenAPI 和 Docker Compose 完整流程

## 下一次对话任务

**M2 第二步：使用 Pydantic v2 设计岗位 API Schema**

学习和实施顺序：

1. 理解 Pydantic Schema 与现有 domain `Job` 的职责差异。
2. 建立 `app/schemas/`，只创建当前需要的岗位 Schema。
3. 定义创建请求、更新请求和响应模型，明确必填、可选和默认字段。
4. 验证空公司、空岗位、非法 URL、非法状态和部分更新语义。
5. 编写 Schema 单元测试，暂不连接 Repository 或数据库。
6. 运行全量测试、Ruff 和 mypy，确认 CLI 与 `/health` 不回归。

默认由用户手动输入代码；除非用户明确要求，否则不要直接修改业务文件。

## 当前已知问题

- `Job.mark_updated()` 当前没有被更新流程使用，但不阻塞 M1 验收。
- `.venv.backup/` 和 `tools/` 是未跟踪本地目录，不属于提交范围。
- M2 `/health` 已通过本地和远程 CI 验证。
- PostgreSQL、SQLAlchemy、Alembic、JWT 和岗位 API 尚未实现。

## Git 说明

```text
分支：main
M1 功能与 README：已推送
M2 /health：已推送
远程 CI：run 30730553236 通过
本地排除：.venv.backup/、tools/
```
