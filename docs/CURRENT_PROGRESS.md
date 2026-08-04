# AI Job Copilot 当前进度

本文件记录当前完成情况、验证证据和下一次任务。

最后核对：2026-08-04

## 当前阶段

**M1 已完成，M2 进行中：`POST /jobs` 已完成**

可靠 Python CLI 已通过 M1 验收。M2 已完成 FastAPI 入口、岗位 Schema 和第一个创建接口；岗位查询、修改、删除、数据库与认证尚未开始。

## M1 已完成

- `Job` dataclass、`JobStatus` enum、UUID、时间字段和输入校验
- Model、Repository、Service、CLI 分层及构造函数依赖注入
- 岗位 CRUD、状态筛选、关键词搜索和重复岗位检测
- JSON 往返和永久保存，临时文件、`fsync`、`os.replace` 安全写入
- `ValidationError`、`JobNotFoundError`、`StorageError` 和 CLI 友好提示
- Model、Service、JSON Repository 的正常与关键异常路径测试
- Fake Repository、pytest fixture、`tmp_path` 和真实数据隔离
- 业务层 80% coverage 门槛、Ruff 和 mypy 严格检查
- GitHub Actions 在 push/PR 时自动执行质量检查
- asyncio JD 练习：顺序执行、`gather()` 并发、异常校验和 4 个测试

## 已验证

- `.venv/bin/python -m compileall -q app examples`：通过
- `.venv/bin/python -m pytest -q`：57 passed
- `.venv/bin/python -m pytest --cov=app.api --cov=app.models --cov=app.schemas --cov=app.services --cov=app.repositories --cov-report=term-missing --cov-fail-under=80`：57 passed
- API、Model、Schema、Service、Repository branch coverage：92.86%，达到 80% 门槛
- `app.api` 独立 coverage：87%，岗位 Router 为 100%
- `app.schemas` 独立 branch coverage：100%
- `.venv/bin/ruff check .`：All checks passed
- `.venv/bin/python -m mypy app examples`：20 个源码文件无问题
- `.venv/bin/python -m pip check`：无依赖冲突
- CLI 输入 `7`：菜单正常显示并退出
- Uvicorn 实际启动：`GET /health` 返回 200，`POST /health` 返回 405，`/docs` 和 OpenAPI 正常
- `.venv/bin/python -m examples.async_jd_fetch`：顺序约 0.90 秒，并发约 0.30 秒
- GitHub Actions run `30797793242`：提交 `bafc206` 状态 `completed / success`

coverage 统计 API、Model、Schema、Service 和 Repository；CLI、`app/main.py` 和 asyncio 示例不计入 92.86%。`POST /jobs`、测试和更新后的 CI 配置已完成本地验证，远程由 GitHub Actions 在 push/PR 时自动验证。

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
- [x] `JobCreate`、`JobUpdate`、`JobResponse` 及正常/异常路径测试
- [x] `POST /jobs`、201/409/422、依赖覆盖和临时数据隔离
- [ ] 岗位查询、修改、删除 API 与其错误映射
- [ ] PostgreSQL、SQLAlchemy 2 和 Alembic
- [ ] 注册、登录、密码哈希和 JWT
- [ ] 用户岗位、时间线、待办和文件的数据隔离
- [ ] 分页、排序、筛选及正常/错误/未认证/越权测试
- [ ] OpenAPI 和 Docker Compose 完整流程

## 下一次对话任务

**M2 第四步：实现 `GET /jobs` 和 `GET /jobs/{job_id}`**

学习和实施顺序：

1. 理解 GET、列表响应、路径参数和 HTTP 404。
2. 为 `GET /jobs` 定义 `list[JobResponse]` 响应。
3. 为 `GET /jobs/{job_id}` 调用 `JobService.get_job()`。
4. 将 `JobNotFoundError` 映射为 404。
5. 测试空列表、已有数据、单条查询和不存在 ID。
6. 运行全量测试、Ruff、mypy 和 API coverage。

默认由用户手动输入代码；除非用户明确要求，否则不要直接修改业务文件。

## 当前已知问题

- `Job.mark_updated()` 当前没有被更新流程使用，但不阻塞 M1 验收。
- `.venv.backup/` 和 `tools/` 是未跟踪本地目录，不属于提交范围。
- PostgreSQL、SQLAlchemy、Alembic、JWT 和其余岗位 API 尚未实现。

## Git 说明

```text
分支：main
M2 /health：已推送
M2 岗位 Schema：已推送
M2 POST /jobs：已完成
远程 CI：GitHub Actions 在 push/PR 时自动运行
本地排除：.venv.backup/、tools/
```
