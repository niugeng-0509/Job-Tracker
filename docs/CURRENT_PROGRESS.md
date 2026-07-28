# AI Job Copilot 当前进度

本文件记录当前完成情况、验证证据和下一次任务

最后核对：2026-07-28

## 当前阶段

**M1：可靠的 Python CLI - CI、asyncio 与文档收尾**

CLI 业务主体、核心自动化测试和本地质量检查已经通过。完成基础 CI、asyncio 小练习和 README 收尾后，才能进入 M2 FastAPI。

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
- `pyproject.toml` 统一 pytest、Ruff、mypy 和 coverage 配置
- Ruff 检查、mypy 严格类型检查和业务层 coverage
- README、项目路线图和完整学习架构指南
- JSON CRUD 代码已推送到 `origin/main`

## 已验证

- `.venv/bin/python -m compileall -q app` 通过
- `python3 -m app.main` 能显示完整菜单并退出
- 临时目录中连续添加、重启读取、修改和删除通过
- 状态筛选、大小写不敏感搜索、重复检测通过
- 错误 ID 显示友好提示
- 损坏 JSON 转换为 `StorageError`，CLI 不显示 traceback
- `.venv/bin/python -m pytest -q`：34 passed
- `.venv/bin/ruff check .`：All checks passed
- `.venv/bin/python -m mypy app`：11 个源码文件无问题
- `.venv/bin/python -m pytest --cov=app.models --cov=app.services --cov=app.repositories --cov-report=term-missing`：34 passed，业务逻辑 branch coverage 92%

coverage 只统计 Model、Service 和 Repository；CLI 与 `main.py` 按当前范围决定保留手工验证，不计入 92%。

## M1 尚未完成

- [x] `Job` Model pytest
- [x] `JobService` pytest
- [x] `JsonJobRepository` pytest 和 `tmp_path`
- [x] 正常路径与关键异常路径测试
- [x] 业务逻辑 coverage 约 80%（实际 92%）
- [x] `pyproject.toml`
- [x] Ruff
- [x] mypy
- [ ] GitHub Actions CI
- [ ] 独立 asyncio 并发获取 JD 练习
- [ ] README 架构说明和终端演示收尾

## 下一次对话任务

**第七天：GitHub Actions 基础 CI**

学习和实施顺序：

1. 理解 workflow、job、step 和干净环境验证。
2. 创建 `.github/workflows/ci.yml`。
3. 配置 Python 3.10 并安装 pytest、pytest-cov、Ruff 和 mypy。
4. 在 CI 运行 Ruff、mypy 和 34 个测试。
5. 对业务逻辑 coverage 设置 80% 最低门槛。
6. 推送后检查 GitHub Actions 的真实结果。
7. 修复本地通过但 CI 失败的环境差异。

默认由用户手动输入代码；除非用户明确要求，否则新对话不要直接修改测试或业务文件。

## 当前已知问题

- `Job.mark_updated()` 当前没有被更新流程使用。
- 部分文件末尾换行等待 Ruff 阶段统一处理。
- 开发工具只安装在本地 `.venv`，CI 和可复现安装尚未完成。
- `resume_output/` 和 `tools/` 不属于 Job Tracker 提交范围。

## Git 说明

```text
分支：main
远程：origin/main
```

提交与远程同步状态每次以实际 `git status` 和 `git log` 为准。

## 进入 M2 的条件

pytest、覆盖率、Ruff、mypy、基础 CI、asyncio 练习和 README 收尾全部完成并验证通过。
