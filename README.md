# Job Tracker

一个使用 Python 构建的命令行求职岗位管理器，也是 AI Job Copilot 项目的 M1 基础版本。当前版本重点练习可靠的业务分层、JSON 持久化、自动测试、静态检查、CI 和 asyncio 并发。

## 当前功能

- 添加、查看、修改和删除岗位
- 按求职状态筛选岗位
- 按公司名称或岗位名称搜索
- 检测公司、岗位名称和链接完全相同的重复记录
- 校验必填字段和招聘链接
- 使用 UUID 标识岗位并记录创建、更新时间
- 将数据永久保存到本地 JSON 文件
- 将业务错误转换为用户可理解的 CLI 提示

岗位状态包括：待投递、已投递、笔试、面试、Offer 和已拒绝。

## 架构与数据流

项目按照职责分层，CLI 不直接读写 JSON，Service 不依赖具体存储实现：

```text
用户输入
   ↓
CLI：读取输入、展示结果、转换友好提示
   ↓
JobService：重复检测、搜索、筛选和 CRUD 业务规则
   ↓
JobRepository Protocol：定义数据访问接口
   ↓
JsonJobRepository：序列化、反序列化和安全文件写入
   ↓
data/jobs.json
```

`Job` Model 负责岗位数据、默认值和字段校验；自定义异常从底层向上传递，最终由 CLI 转换成用户提示。Repository 通过构造函数注入 `JobService`，因此测试时可以替换成 Fake Repository，不会操作真实业务数据。

JSON 保存采用“同目录临时文件 → `flush` → `fsync` → `os.replace`”流程，避免写入过程中断后直接损坏正式文件。损坏的 JSON 会转换成 `StorageError`，不会被读取流程覆盖。

## 项目结构

```text
.
├── .github/workflows/
│   └── ci.yml                       # GitHub Actions 质量检查
├── app/
│   ├── models/                      # Job 数据模型和状态枚举
│   ├── repositories/                # Repository 接口和 JSON 实现
│   ├── services/                    # 岗位业务逻辑
│   ├── cli.py                       # 命令行交互
│   ├── exceptions.py                # 自定义异常
│   └── main.py                      # 依赖组装和程序入口
├── examples/
│   └── async_jd_fetch.py            # asyncio 顺序/并发获取 JD 练习
├── tests/
│   ├── test_job.py                  # Model 测试
│   ├── test_job_service.py          # Service 测试
│   ├── test_json_job_repository.py  # JSON Repository 测试
│   └── test_async_jd_fetch.py       # asyncio 练习测试
├── docs/                            # 进度、路线图和学习指南
├── pyproject.toml                   # pytest、Ruff、mypy、coverage 配置
└── README.md
```

## 运行环境

- Python 3.10 或更高版本
- 当前业务运行只使用 Python 标准库
- pytest、pytest-cov、Ruff 和 mypy 仅用于开发与验证

## 安装开发环境

在项目根目录创建并启用虚拟环境：

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Windows PowerShell 使用：

```powershell
.venv\Scripts\Activate.ps1
```

安装开发工具：

```bash
python -m pip install --upgrade pip
python -m pip install "pytest>=9.0" "pytest-cov>=7.0" "ruff>=0.15" "mypy>=2.0"
```

## 运行 CLI

```bash
python -m app.main
```

启动后会显示：

```text
===== Job Tracker =====
1. 添加岗位
2. 查看全部岗位
3. 修改岗位
4. 删除岗位
5. 按状态筛选
6. 搜索岗位
7. 退出
请选择：
```

岗位数据默认保存在 `data/jobs.json`。该文件属于本地运行数据，已经被 Git 忽略，不应提交到仓库。

## asyncio JD 练习

运行独立示例：

```bash
python -m examples.async_jd_fetch
```

示例使用 `asyncio.sleep()` 模拟外部 I/O，不访问真实网站。三个岗位逐个等待约需 0.90 秒，使用 `asyncio.gather()` 并发调度约需 0.30 秒：

```text
顺序获取 3 个 JD，耗时：0.90 秒
并发获取 3 个 JD，耗时：0.30 秒
```

这个示例展示 coroutine、Task、事件循环、`await` 和非阻塞并发的基本关系，不属于当前 CLI 的生产数据流程。

## 测试与质量检查

运行全部测试：

```bash
python -m pytest -q
```

当前测试套件共 38 个测试，覆盖 Model、Service、JSON Repository 和 asyncio 练习。Repository 测试使用 pytest 的 `tmp_path`，不会读写真实的 `data/jobs.json`。

运行 Ruff：

```bash
ruff check .
```

运行类型检查：

```bash
python -m mypy app examples
```

检查业务层覆盖率，并要求不低于 80%：

```bash
python -m pytest \
  --cov=app.models \
  --cov=app.services \
  --cov=app.repositories \
  --cov-report=term-missing \
  --cov-fail-under=80
```

最近一次本地验证为 38 tests passed，业务层 branch coverage 91.50%。覆盖率只统计 Model、Service 和 Repository，不包括 CLI、`main.py` 和示例代码。

## 持续集成

`.github/workflows/ci.yml` 会在推送到 `main` 或向 `main` 创建 Pull Request 时，在干净的 Ubuntu 和 Python 3.10 环境中自动执行：

1. Ruff 代码检查
2. `app` 类型检查
3. 全部 pytest 测试
4. Model、Service、Repository 的 80% coverage 门槛

任意步骤失败，CI 都会失败，从而帮助发现环境依赖、类型错误、测试回归和覆盖率下降。

## 项目文档

| 文档 | 作用 |
| --- | --- |
| [AGENTS.md](AGENTS.md) | Codex 的检查、教学、修改和验证规则 |
| [当前进度](docs/CURRENT_PROGRESS.md) | 当前完成情况、验证证据和下一次任务 |
| [里程碑路线图](docs/PROJECT_ROADMAP.md) | M1-M9 的交付顺序和退出条件 |
| [学习与架构指南](docs/AI_JOB_COPILOT_LEARNING_GUIDE.md) | 详细知识、系统架构和学习方法 |

当前实现是 AI Job Copilot 的可靠 CLI 基础。后续里程碑会在通过 M1 验收后继续增加 FastAPI、数据库、LLM、RAG 和 Agent 能力；这些功能尚未包含在当前版本中。
