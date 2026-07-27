# AI Job Copilot 当前进度

本文件记录当前完成情况、验证证据和下一次任务

最后核对：2026-07-27

## 当前阶段

**M1：可靠的 Python CLI - 测试与工程配置收尾**

CLI 业务主体已完成并经过手工验证，`Job` Model 已有第一组自动化测试。完成 Service、Repository 测试、代码质量检查、CI 和 asyncio 小练习后，才能进入 M2 FastAPI。

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
- README、项目路线图和完整学习架构指南
- JSON CRUD 代码已推送到 `origin/main`

## 已验证

- `python3 -m compileall -q app` 通过
- `python3 -m app.main` 能显示完整菜单并退出
- 临时目录中连续添加、重启读取、修改和删除通过
- 状态筛选、大小写不敏感搜索、重复检测通过
- 错误 ID 显示友好提示
- 损坏 JSON 转换为 `StorageError`，CLI 不显示 traceback
- `python -m pytest -v` 通过，共 15 个测试

CLI 和持久化流程仍主要是手工与临时脚本验证；`Job` Model 已形成 pytest 回归测试。

## M1 尚未完成

- [x] `Job` Model pytest
- [ ] `JobService` pytest
- [ ] `JsonJobRepository` pytest 和 `tmp_path`
- [ ] 正常路径与关键异常路径测试
- [ ] coverage 约 80%
- [ ] `pyproject.toml`
- [ ] Ruff
- [ ] mypy
- [ ] GitHub Actions CI
- [ ] 独立 asyncio 并发获取 JD 练习
- [ ] README 架构说明和终端演示收尾

## 下一次对话任务

**第四天：Fake Repository 与 `JobService` 单元测试**

学习和实施顺序：

1. 理解 Fake、依赖注入和 Service 单元测试边界。
2. 创建只保存在内存中的 Fake Repository。
3. 测试添加、查询、修改和删除。
4. 测试状态筛选和大小写不敏感搜索。
5. 测试重复岗位和空搜索关键词。
6. 验证测试不读写真实 `data/jobs.json`。
7. 运行单文件和全部测试。

默认由用户手动输入代码；除非用户明确要求，否则新对话不要直接修改测试或业务文件。

## 当前已知问题

- `app/cli.py` 有未使用的 `ValidationError` import。
- `Job.mark_updated()` 当前没有被更新流程使用。
- 部分文件末尾换行等待 Ruff 阶段统一处理。
- `JobService` 和 `JsonJobRepository` 尚无自动化测试。
- `resume_output/` 和 `tools/` 不属于 Job Tracker 提交范围。

## Git 快照

```text
分支：main
远程：origin/main
最新业务提交：95bdd4b
feat: add JSON persistence and job CRUD operations
```

开始新对话时仍需检查实际 `git status`、代码和测试；实际结果优先于本文件。

## 进入 M2 的条件

pytest、覆盖率、Ruff、mypy、基础 CI、asyncio 练习和 README 收尾全部完成并验证通过。
