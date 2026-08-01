# AI Job Copilot 当前进度

本文件记录当前完成情况、验证证据和下一次任务。

最后核对：2026-08-01

## 当前阶段

**M1 已完成：准备进入 M2 FastAPI 多用户后端**

可靠 Python CLI 的功能、异常、JSON 持久化、分层、自动测试、质量门槛、基础 CI、asyncio 练习和 README 均已完成。包含全部 38 个测试的远程 CI 已通过，M1 退出条件满足；M2 尚未开始。

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
- `.venv/bin/python -m pytest --cov=app.models --cov=app.services --cov=app.repositories --cov-report=term-missing --cov-fail-under=80`：38 passed
- 业务逻辑 branch coverage：91.50%，达到 80% 门槛
- `.venv/bin/ruff check .`：All checks passed
- `.venv/bin/python -m mypy app examples`：13 个源码文件无问题
- `.venv/bin/python -m examples.async_jd_fetch`：顺序约 0.90 秒，并发约 0.30 秒
- GitHub Actions run `30693228223`：提交 `b589914` 状态 `completed / success`

coverage 只统计 Model、Service 和 Repository；CLI、`main.py` 和 asyncio 示例不计入 91.50%。CI 已实际收集并运行全部 38 个测试。

## M1 验收

- [x] CLI 正常路径和关键异常路径可靠
- [x] JSON 安全持久化，不覆盖损坏文件
- [x] 测试不操作真实 `data/jobs.json`
- [x] 业务逻辑 coverage 超过 80%
- [x] Ruff、mypy 和 pytest 通过
- [x] 基础 GitHub Actions CI 通过
- [x] 独立 asyncio 并发练习通过
- [x] README 可指导安装、运行和测试

## M2 尚未完成

- [ ] FastAPI 应用骨架和 `/health` 接口
- [ ] 岗位请求/响应 Pydantic 模型和 CRUD API
- [ ] PostgreSQL、SQLAlchemy 2 和 Alembic
- [ ] 注册、登录、密码哈希和 JWT
- [ ] 用户岗位、时间线、待办和文件的数据隔离
- [ ] 分页、排序、筛选及正常/错误/未认证/越权测试
- [ ] OpenAPI 和 Docker Compose 完整流程

## 下一次对话任务

**M2 第一步：建立最小 FastAPI 应用并完成 `/health` 测试**

学习和实施顺序：

1. 理解 HTTP 请求/响应、状态码、ASGI 和 FastAPI 应用入口。
2. 确定 M2 目录边界，暂不引入数据库、JWT 或岗位 CRUD。
3. 安装并记录 FastAPI、Uvicorn、httpx 等本阶段基础依赖。
4. 手动创建最小应用和 `GET /health`，返回明确的 JSON 响应。
5. 使用 FastAPI TestClient 编写正常路径测试。
6. 运行服务、接口测试、Ruff 和 mypy，确认 CLI 原有 38 个测试不回归。

默认由用户手动输入代码；除非用户明确要求，否则不要直接修改业务文件。

## 当前已知问题

- `Job.mark_updated()` 当前没有被更新流程使用，但不阻塞 M1 验收。
- `.venv.backup/` 和 `tools/` 是未跟踪本地目录，不属于提交范围。
- M2 的依赖管理、API 目录和数据库方案尚未实现，应从最小 `/health` 开始。

## Git 说明

```text
分支：main
M1 功能与 README：已推送
远程 CI：38 个测试通过
本地排除：.venv.backup/、tools/
```
