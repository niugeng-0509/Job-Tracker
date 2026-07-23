# Job Tracker

一个用于练习 Python 基础的命令行求职投递管理器。

## 当前功能

- 添加岗位
- 查看全部岗位
- 退出程序

目前数据保存在内存中，退出程序后会清空。后续学习 JSON 时再增加永久保存功能。

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

## 第一阶段升级路线

1. 增加输入校验、删除和状态筛选
2. 使用 `dataclass` 定义岗位模型
3. 增加类型注解和自定义异常
4. 使用 JSON 保存和读取岗位
5. 使用 pytest 编写自动测试
6. 通过独立练习理解 asyncio

完整的 AI 大模型开发项目演进计划见
[docs/PROJECT_ROADMAP.md](docs/PROJECT_ROADMAP.md)。
