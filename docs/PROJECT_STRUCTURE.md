# Passgate 票务系统 · 项目目录结构

> 前后端分离：Vue 3 前端 + Python FastAPI 后端 · Monorepo 结构

---

## 整体结构概览

```
passgate/
├── frontend/                 # Vue 3 前端应用
├── backend/                  # Python FastAPI 后端应用
├── docs/                     # 项目文档（PRD、原型图、TODO 等）
├── docker/                   # Docker 相关配置（可选）
└── README.md
```

---

## 一、前端目录结构 (frontend/)

```
frontend/
├── public/                       # 静态资源（不参与构建）
│   └── favicon.ico
│
├── src/
│   ├── main.js                   # 入口文件
│   ├── App.vue                   # 根组件（含 Tab 路由布局）
│   │
│   ├── api/                      # API 接口封装
│   │   ├── index.js              # axios 实例、拦截器
│   │   ├── auth.js               # 登录、修改密码
│   │   ├── movies.js             # 电影相关接口
│   │   ├── tickets.js            # 票务出票、核销、作废
│   │   └── stats.js              # 今日统计
│   │
│   ├── assets/                   # 构建时引用的静态资源
│   │   ├── images/
│   │   └── styles/
│   │       └── variables.less     # 主题变量（配合 Vant）
│   │
│   ├── components/               # 公共组件
│   │   ├── Layout/
│   │   │   ├── TabBar.vue        # 底部 Tab 导航
│   │   │   └── NavBar.vue        # 顶部导航栏
│   │   ├── TicketCard.vue        # 票务卡片（历史列表用）
│   │   ├── QRDisplay.vue         # 二维码展示区域
│   │   └── VerifyResultModal.vue # 核销结果弹窗
│   │
│   ├── views/                    # 页面级组件
│   │   ├── Login/                # 登录页（独立，无 Tab）
│   │   │   └── index.vue
│   │   │
│   │   ├── Issue/                # Tab 1 出票
│   │   │   ├── index.vue         # 出票主页面
│   │   │   ├── MovieDrawer.vue   # 管理电影左侧抽屉
│   │   │   ├── MovieForm.vue     # 新增/编辑电影表单
│   │   │   ├── IssueHistory.vue  # 出票历史页
│   │   │   └── TicketDetail.vue  # 票务详情 Sheet
│   │   │
│   │   ├── Verify/               # Tab 2 检票
│   │   │   ├── index.vue         # 检票主页面（开始检票按钮）
│   │   │   ├── ScannerPage.vue   # 全屏扫码页面
│   │   │   └── VerifyHistory.vue # 检票历史页
│   │   │
│   │   └── Profile/              # Tab 3 个人
│   │       ├── index.vue         # 个人主页（头像、今日数据、菜单）
│   │       └── ChangePassword.vue # 修改密码页
│   │
│   ├── router/
│   │   └── index.js              # Vue Router 配置、路由守卫、Tab 匹配
│   │
│   ├── store/                    # Pinia 状态管理
│   │   ├── index.js
│   │   ├── user.js               # 用户信息、Token、角色
│   │   └── app.js                # 全局状态（如需）
│   │
│   ├── utils/
│   │   ├── auth.js               # Token 存取、过期校验
│   │   ├── phone.js              # 手机号脱敏（138****8888）
│   │   └── validator.js          # 表单校验规则
│   │
│   └── composables/              # 组合式函数（可选）
│       └── useQRScanner.js       # 扫码逻辑封装
│
├── index.html
├── vite.config.js
├── package.json
└── .env.example                 # 环境变量示例（API_BASE_URL 等）
```

### 前端技术栈

| 依赖 | 用途 |
|------|------|
| Vue 3 | 框架 |
| Vite | 构建工具 |
| Vue Router | 路由 |
| Pinia | 状态管理 |
| Vant 4 | 移动端 UI 组件库 |
| Axios | HTTP 请求 |
| html5-qrcode 或 vue-qrcode-reader | 二维码扫码 |

---

## 二、后端目录结构 (backend/)

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                   # FastAPI 应用入口
│   ├── config.py                 # 配置（数据库、JWT、环境）
│   │
│   ├── core/                     # 核心模块
│   │   ├── __init__.py
│   │   ├── security.py           # 密码哈希、JWT 生成与校验
│   │   └── database.py           # SQLAlchemy 引擎、Session、Base
│   │
│   ├── models/                   # ORM 模型
│   │   ├── __init__.py
│   │   ├── staff.py              # 工作人员表
│   │   ├── movie.py              # 电影促销表
│   │   └── ticket.py             # 票务表
│   │
│   ├── schemas/                  # Pydantic 请求/响应模型
│   │   ├── __init__.py
│   │   ├── auth.py               # LoginRequest, TokenResponse
│   │   ├── movie.py              # MovieCreate, MovieResponse
│   │   ├── ticket.py             # TicketCreate, TicketResponse, VerifyResult
│   │   └── common.py             # 分页、通用响应
│   │
│   ├── api/                      # 路由层
│   │   ├── __init__.py
│   │   ├── deps.py               # 依赖注入：get_current_user 等
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── router.py         # 汇总所有子路由
│   │       ├── auth.py           # /api/auth/login, change-password
│   │       ├── movies.py         # /api/movies/*
│   │       ├── tickets.py        # /api/tickets/*
│   │       └── stats.py          # /api/stats/today
│   │
│   ├── services/                 # 业务逻辑层
│   │   ├── __init__.py
│   │   ├── auth_service.py       # 登录校验、修改密码
│   │   ├── movie_service.py      # 电影 CRUD、下架
│   │   ├── ticket_service.py     # 出票、核销、作废、历史
│   │   └── qrcode_service.py     # 二维码生成（Base64）
│   │
│   └── crud/                     # 数据访问层（可选，或合并到 services）
│       ├── __init__.py
│       ├── staff.py
│       ├── movie.py
│       └── ticket.py
│
├── alembic/                      # 数据库迁移（可选）
│   ├── env.py
│   ├── versions/
│   └── alembic.ini
│
├── scripts/                      # 脚本
│   ├── init_db.py                # 初始化数据库、创建初始管理员
│   └── seed_movies.py            # 示例数据（可选）
│
├── tests/                        # 单元/集成测试
│   ├── __init__.py
│   ├── conftest.py               # pytest fixtures
│   ├── test_auth.py
│   ├── test_movies.py
│   ├── test_tickets.py
│   └── test_verify.py
│
├── requirements.txt
├── .env.example                  # 环境变量示例
└── README.md
```

### 后端技术栈

| 依赖 | 用途 |
|------|------|
| FastAPI | Web 框架 |
| SQLAlchemy 2.x | ORM |
| Pydantic v2 | 数据校验与序列化 |
| python-jose / PyJWT | JWT |
| passlib[bcrypt] | 密码哈希 |
| qrcode + pillow | 二维码生成 |
| python-multipart | 表单解析 |
| uvicorn | ASGI 服务器 |

---

## 三、接口与目录对应关系

| PRD 接口 | 后端文件 | 前端 API 文件 |
|----------|----------|---------------|
| POST /api/auth/login | api/v1/auth.py | api/auth.js |
| POST /api/auth/change-password | api/v1/auth.py | api/auth.js |
| GET /api/movies/active | api/v1/movies.py | api/movies.js |
| GET/POST /api/movies | api/v1/movies.py | api/movies.js |
| PUT /api/movies/:id | api/v1/movies.py | api/movies.js |
| POST /api/movies/:id/deactivate | api/v1/movies.py | api/movies.js |
| POST /api/tickets | api/v1/tickets.py | api/tickets.js |
| GET /api/tickets | api/v1/tickets.py | api/tickets.js |
| POST /api/tickets/:id/void | api/v1/tickets.py | api/tickets.js |
| POST /api/tickets/verify | api/v1/tickets.py | api/tickets.js |
| GET /api/tickets/check-history | api/v1/tickets.py | api/tickets.js |
| GET /api/stats/today | api/v1/stats.py | api/stats.js |

---

## 四、开发与部署

### 本地开发

```bash
# 后端（默认 8000）
cd backend && pip install -r requirements.txt && uvicorn app.main:app --reload

# 前端（默认 5173）
cd frontend && npm install && npm run dev
```

前端通过 Vite 代理或环境变量 `VITE_API_BASE_URL` 指向后端。

### 生产部署

- **前端**：`npm run build` 生成 `dist/`，部署至 Nginx 静态目录
- **后端**：uvicorn + gunicorn 部署
- **数据库**：MySQL，使用 `scripts/init_db.py` 初始化表结构与初始账号

---

## 五、环境变量示例

### backend/.env.example

```
DATABASE_URL=mysql+pymysql://user:pass@localhost:3306/passgate
SECRET_KEY=your-jwt-secret-key
JWT_EXPIRE_DAYS=7
```

### frontend/.env.example

```
VITE_API_BASE_URL=http://localhost:8000
```

---

*根据 PRD.md v1.2 与 原型图_三页面.html 整理 · 可直接作为开发规范*
