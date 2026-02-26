# Passgate Backend

FastAPI 后端，票务系统 API。

## 快速开始

```bash
# 安装依赖
pip install -r requirements.txt

# 配置环境变量（复制 .env.example 为 .env）

# 初始化数据库（需先创建 MySQL 库 passgate）
python -m scripts.init_db

# 启动服务
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## 默认账号

- 账号: admin
- 密码: admin123
