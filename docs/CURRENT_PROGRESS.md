# AI Job Copilot 当前进度

本文件记录当前完成情况、验证证据和下一次任务

最后核对：2026-07-27

## 当前阶段

**M1：可靠的 Python CLI - 测试与工程配置收尾**

CLI 业务主体已完成并经过手工验证，Model、Service 和 JSON Repository 已有自动化测试。完成代码质量检查、CI 和 asyncio 小练习后，才能进入 M2 FastAPI。

## 已完成

- `Job` dataclass、`JobStatus` enum、UUID 和时间字段
- 公司/岗位非空校验、URL 校验和输入清理
- Model、Repository、Service、CLI 分层
- `JobRepository` Protocol 和构造函数依赖注入
- 岗位添加、查看、修改、删除
- 状态筛选、关键词搜索和重复岗位检测
- JSON 序列化、反序列化和永久保存
- 临时文件、`fsync`、`os.replace` 安全写入
- `ValidationError`、`JobNotFoundError`、`StorageError`
- CLI 友好错误提示和删除确认
- `Job` Model 的正常、默认值、输入清理和校验测试
- Fake Repository、pytest fixture 和 `JobService` 核心业务测试
- `tmp_path` 隔离、JSON 往返、CRUD 和损坏文件测试
- README、项目路线图和完整学习架构指南
- JSON CRUD 代码已推送到 `origin/main`

## 已验证

- `python3 -m compileall -q app` 通过
- `python3 -m app.main` 能显示完整菜单并退出
- 临时目录中连续添加、重启读取、修改和删除通过
- 状态筛选、大小写不敏感搜索、重复检测通过
- 错误 ID 显示友好提示
- 损坏 JSON 转换为 `StorageError`，CLI 不显示 traceback
- `.venv/bin/python -m compileall -q app` 通过
- `.venv/bin/python -m pytest tests/test_job_service.py -v` 通过，11 个测试
- `.venv/bin/python -m pytest tests/test_json_job_repository.py -q` 通过，8 个测试
- `.venv/bin/python -m pytest -q` 通过，共 34 个测试

CLI 交互仍主要是手工验证；Model、Service 和 JSON Repository 已形成 pytest 回归测试。

## M1 尚未完成

- [x] `Job` Model pytest
- [x] `JobService` pytest
- [x] `JsonJobRepository` pytest 和 `tmp_path`
- [x] 正常路径与关键异常路径测试
- [ ] coverage 约 80%
- [ ] `pyproject.toml`
- [ ] Ruff
- [ ] mypy
- [ ] GitHub Actions CI
- [ ] 独立 asyncio 并发获取 JD 练习
- [ ] README 架构说明和终端演示收尾

## 下一次对话任务

**第六天：`pyproject.toml`、Ruff、mypy 和 coverage**

学习和实施顺序：

1. 理解统一工程配置、lint、类型检查和覆盖率的职责。
2. 创建最小 `pyproject.toml`，配置 pytest、Ruff 和 mypy。
3. 安装 Ruff、mypy 和 pytest-cov 开发工具。
4. 运行 `ruff check .` 和 `mypy app`，修复实际问题。
5. 运行 coverage，记录真实结果并定位核心缺口。
6. 补充必要测试，不为追求数字测试无价值细节。
7. 运行全部检查并确认 34 个现有测试继续通过。

默认由用户手动输入代码；除非用户明确要求，否则新对话不要直接修改测试或业务文件。

## 当前已知问题

- `app/cli.py` 有未使用的 `ValidationError` import。
- `Job.mark_updated()` 当前没有被更新流程使用。
- 部分文件末尾换行等待 Ruff 阶段统一处理。
- `resume_output/` 和 `tools/` 不属于 Job Tracker 提交范围。

## Git 说明

```text
分支：main
远程：origin/main
```

提交与远程同步状态每次以实际 `git status` 和 `git log` 为准。

## 进入 M2 的条件

pytest、覆盖率、Ruff、mypy、基础 CI、asyncio 练习和 README 收尾全部完成并验证通过。
