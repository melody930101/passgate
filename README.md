# Passgate · 电影院学生优惠票务系统

工作人员端 H5，前后端分离：Vue 3 前端 + Python FastAPI 后端。

## 项目结构

```
passgate/
├── frontend/      # Vue 3 + Vite + Vant
├── backend/       # FastAPI + SQLAlchemy + MySQL
├── docs/          # 项目文档
│   ├── PRD.md             # 产品需求文档
│   ├── 原型图_三页面.html  # 三页面原型
│   ├── PROJECT_STRUCTURE.md  # 目录结构说明
│   └── TODO.md            # 待完成计划
└── README.md
```

## 快速开始

### 1. 后端

```bash
cd backend
pip install -r requirements.txt
# 配置 .env（参考 .env.example）
python -m scripts.init_db   # 初始化数据库
uvicorn app.main:app --reload --port 8000
```

默认管理员：`admin` / `admin123`

### 2. 前端

```bash
cd frontend
npm install
npm run dev
```

访问 http://localhost:5173

## 部署（Docker）

```bash
# 配置 backend/.env（DATABASE_URL 指向云 MySQL）
docker compose up -d --build
```

需配合 Nginx 做 HTTPS 终止与反向代理（见 [docs/nginx-ai-melody.conf](docs/nginx-ai-melody.conf)）。

**日常更新**：`git pull` 后执行 `docker compose up -d --build`
