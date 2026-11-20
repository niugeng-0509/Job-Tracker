# Job Tracker

一个使用 Python 构建的求职管理项目。M1 CLI 和 M2 多用户 FastAPI 后端已经实现，提供 PostgreSQL 持久化、JWT 认证、岗位管理、投递时间线、待办和文件元数据管理。

## 当前功能

- 添加、查看、修改和删除岗位
- 按求职状态筛选岗位
- 按公司名称或岗位名称搜索
- 检测公司、岗位名称和链接完全相同的重复记录
- 校验必填字段和招聘链接
- 使用 UUID 标识岗位并记录创建、更新时间
- 将数据永久保存到本地 JSON 文件
- 将业务错误转换为用户可理解的 CLI 提示
- 提供 FastAPI 应用入口和 `GET /health` 健康检查
- 注册、登录、Argon2 密码哈希和带过期时间的 JWT
- 带用户隔离的岗位 CRUD、分页、排序、状态与关键词组合筛选
- 投递时间线、待办任务和受类型、内容、大小限制的文件上传
- SQLAlchemy 2 ORM、Alembic 迁移、PostgreSQL 和 Docker Compose
- 自动生成 OpenAPI、Swagger UI 和 ReDoc 文档

岗位状态包括：待投递、已投递、笔试、面试、Offer 和已拒绝。

## 架构与数据流

项目把正式后端与历史学习示例分开：`app/` 是 M2 及后续正式主线，`examples/m1_cli/` 完整保留 M1 CLI。

```text
用户输入
   ↓
M1 CLI 示例：读取输入、展示结果、转换友好提示
   ↓
JobService：重复检测、搜索、筛选和 CRUD 业务规则
   ↓
JobRepository Protocol：定义数据访问接口
   ↓
JsonJobRepository：序列化、反序列化和安全文件写入
   ↓
data/jobs.json

正式 HTTP 客户端
   ↓
Router：接收 HTTP 参数并返回响应，不访问数据库
   ↓
Service：认证、重复检测、所有权和文件规则
   ↓
Unit of Work：统一一次业务操作的事务边界
   ↓
Repository Protocol：定义数据访问契约
   ↓
SQLAlchemy Repository：查询强制包含 user_id
   ↓
PostgreSQL：User、Job、ApplicationEvent、Task、Document
```

正式后端中，Pydantic Schema 只负责 API 输入输出，SQLAlchemy Model 只负责数据库映射，Service 负责业务规则。Service 依赖 `UnitOfWork` 和 Repository Protocol，不依赖具体 SQLAlchemy Repository；领域异常由 FastAPI 统一转换为 HTTP 状态码。这样 Router、业务规则、查询和事务可以分别测试。

JSON 保存采用“同目录临时文件 → `flush` → `fsync` → `os.replace`”流程，避免写入过程中断后直接损坏正式文件。损坏的 JSON 会转换成 `StorageError`，不会被读取流程覆盖。

## 项目结构

```text
.
├── .github/workflows/
│   └── ci.yml                       # GitHub Actions 质量检查
├── app/                             # M2 及后续正式后端
│   ├── api/
│   │   ├── dependencies/            # Session、服务组装和当前用户依赖
│   │   ├── routes/                  # 轻量 HTTP Router
│   │   └── exception_handlers.py    # 领域异常到 HTTP 的统一映射
│   ├── core/                        # 配置和 JWT/密码安全
│   ├── db/                          # Session、ORM Model 和 Unit of Work
│   ├── domain/                      # 业务枚举和领域异常
│   ├── repositories/                # 数据访问 Protocol 与 SQLAlchemy 实现
│   ├── schemas/                     # 按资源拆分的 Pydantic Schema
│   ├── services/                    # 认证、岗位、事件、待办、文件业务
│   └── main.py                      # 正式 FastAPI 入口
├── examples/
│   └── m1_cli/                      # M1 CLI、JSON Repository 和 asyncio
├── tests/
│   ├── examples/m1_cli/             # M1 示例完整测试
│   ├── test_health.py               # FastAPI 健康检查测试
│   ├── test_job_schemas.py          # 岗位 API Schema 测试
│   ├── test_jobs_api.py             # 完整 API 接口测试
│   ├── test_repositories.py         # SQLAlchemy Repository 集成测试
│   └── test_services.py             # Service 与事务单元测试
├── docs/                            # 进度、路线图和学习指南
├── pyproject.toml                   # pytest、Ruff、mypy、coverage 配置
├── requirements.txt                 # 应用运行依赖
├── requirements-dev.txt             # 测试和质量检查依赖
└── README.md
```

## 运行环境

- Python 3.10 或更高版本
- CLI 业务核心只使用 Python 标准库
- FastAPI 和 Uvicorn 用于 Web API
- HTTPX2、pytest、pytest-cov、Ruff 和 mypy 用于开发与验证

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

安装应用和开发依赖：

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements-dev.txt
```

## 运行 CLI

```bash
python -m examples.m1_cli.main
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

## 运行 FastAPI

启动开发服务器：

```bash
python -m uvicorn app.main:app --reload
```

健康检查：

```bash
curl http://127.0.0.1:8000/health
```

预期响应：

```json
{"status":"ok"}
```

交互式文档和 OpenAPI Schema：

```text
http://127.0.0.1:8000/docs
http://127.0.0.1:8000/redoc
http://127.0.0.1:8000/openapi.json
```

当前 `/health` 只检查 API 进程能否响应，不执行数据库查询。

## PostgreSQL 与 Docker Compose

复制并修改环境变量后启动完整环境：

```bash
cp .env.example .env
docker compose up --build
```

非容器环境先设置 `DATABASE_URL` 和 `JWT_SECRET`，再执行：

```bash
alembic upgrade head
python -m uvicorn app.main:app --reload
```

在 `/docs` 中先调用 `POST /auth/register`，再使用 Authorize 表单登录。除注册、登录和健康检查外，业务接口都要求 Bearer Token。

## asyncio JD 练习

运行独立示例：

```bash
python -m examples.m1_cli.async_jd_fetch
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

当前测试套件共 58 个测试，覆盖认证、用户隔离、API、Model、Schema、Service、Unit of Work、SQLAlchemy/JSON Repository 和 asyncio 练习。API 集成测试使用独立 SQLite 数据库和临时上传目录，不接触本地业务数据。

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
  --cov=app \
  --cov=examples.m1_cli.models \
  --cov=examples.m1_cli.services \
  --cov=examples.m1_cli.repositories \
  --cov-report=term-missing \
  --cov-fail-under=80
```

最近一次本地验证为 58 tests passed，正式后端与 M1 核心层 branch coverage 为 93.76%。覆盖率不包括交互式 CLI、M1 入口和 asyncio 演示代码。

## 持续集成

`.github/workflows/ci.yml` 会在推送到 `main` 或向 `main` 创建 Pull Request 时，在干净的 Ubuntu 和 Python 3.10 环境中自动执行：

1. Ruff 代码检查
2. `app` 类型检查
3. 全部 pytest 测试
4. API、Model、Schema、Service、Repository 的 80% coverage 门槛

任意步骤失败，CI 都会失败，从而帮助发现环境依赖、类型错误、测试回归和覆盖率下降。

## 项目文档

| 文档 | 作用 |
| --- | --- |
| [AGENTS.md](AGENTS.md) | Codex 的检查、教学、修改和验证规则 |
| [当前进度](docs/CURRENT_PROGRESS.md) | 当前完成情况、验证证据和下一次任务 |
| [里程碑路线图](docs/PROJECT_ROADMAP.md) | M1-M9 的交付顺序和退出条件 |
| [学习与架构指南](docs/AI_JOB_COPILOT_LEARNING_GUIDE.md) | 详细知识、系统架构和学习方法 |

当前实现已覆盖 M2 多用户后端代码范围。下一阶段是 M3 LLM 岗位分析与聊天；本机未安装 Docker CLI，因此容器实际启动仍需在有 Docker 的环境验证。
