# Job Tracker

一个用于练习 Python 基础的命令行求职投递管理器。

## 当前功能

- 添加岗位
- 查看全部岗位
- 修改岗位
- 删除岗位
- 按状态筛选
- 按公司名称或岗位名称搜索
- JSON 永久保存
- 重复岗位检测

## 项目结构

```text
app/
├── models/          # 岗位数据模型
├── repositories/    # JSON 数据访问
├── services/        # 业务逻辑
├── cli.py           # 命令行交互
├── exceptions.py    # 自定义异常
└── main.py          # 程序入口
```

## 运行环境

- Python 3.10 或更高版本

## 开始运行

创建并启用虚拟环境：

```bash
python3 -m venv .venv
source .venv/bin/activate
```

运行程序：

```bash
python -m app.main
```

运行测试：

```bash
python -m pip install pytest
python -m pytest -v
```

## 项目文档

| 文档 | 作用 | 更新频率 |
| --- | --- | --- |
| [AGENTS.md](AGENTS.md) | Codex 的检查、教学、修改和验证规则 | 协作方式改变时 |
| [当前进度](docs/CURRENT_PROGRESS.md) | 当前完成情况、验证证据和下一次任务 | 每天结束时 |
| [里程碑路线图](docs/PROJECT_ROADMAP.md) | M1-M9 的顺序、交付和退出条件 | 阶段计划改变时 |
| [学习与架构指南](docs/AI_JOB_COPILOT_LEARNING_GUIDE.md) | 详细知识、系统架构、学习方法和面试参考 | 长期设计改变时 |
