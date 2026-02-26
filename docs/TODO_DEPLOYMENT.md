# Passgate · 部署上线 详细 To-Do

> 依据 [TODO.md](./TODO.md) 第七节、[PRD.md](./PRD.md) 4.1 技术选型整理

---

## 一、前置准备

| 状态 | 任务 | 说明 |
|:----:|------|------|
| ⬜ | 购买云服务器 | 建议 2 核 2G（阿里云/腾讯云/华为云轻量，约 100 元/月） |
| ⬜ | 购买域名 | 需备案（国内服务器） |
| ⬜ | 域名备案 | 国内服务器必须，流程约 1～2 周 |
| ⬜ | 准备 MySQL | 本机安装或云 RDS；提前建库 `passgate` |

---

## 二、服务器环境

| 状态 | 任务 | 说明 |
|:----:|------|------|
| ⬜ | 安装 Nginx | `apt install nginx` 或 `yum install nginx` |
| ⬜ | 安装 MySQL | 若不自建则跳过 |
| ⬜ | 安装 Python 3.10+ | 建议 3.10/3.11，避免 bcrypt 与 3.13 兼容问题 |
| ⬜ | 设置时区 | 服务器 `TZ=Asia/Shanghai` 或 `timedatectl set-timezone Asia/Shanghai` |
| ⬜ | MySQL 时区 | 配置 `time_zone='+08:00'` 或 `Asia/Shanghai` |
| ⬜ | 防火墙放行 | 443（HTTPS）、80（可选）、22（SSH） |

---

## 三、环境变量与安全

| 状态 | 任务 | 说明 |
|:----:|------|------|
| ⬜ | 生成 SECRET_KEY | `openssl rand -hex 32`，写入 `backend/.env` |
| ⬜ | 配置 DATABASE_URL | 生产库地址、用户名、强密码 |
| ⬜ | 配置 CORS_ORIGINS | 建议 `['https://你的域名']` 替代 `*` |
| ⬜ | 配置 TIMEZONE | 保持 `Asia/Shanghai` |
| ⬜ | 保护 .env | 确保 `.env` 不被提交，仅在服务器本地 |

---

## 四、数据库

| 状态 | 任务 | 说明 |
|:----:|------|------|
| ⬜ | 创建数据库 | `CREATE DATABASE passgate CHARACTER SET utf8mb4;` |
| ⬜ | 执行 init_db | `python -m scripts.init_db`，创建表 + 默认管理员 |
| ⬜ | 验证管理员 | 确认 `admin` / `admin123` 可登录（上线后改密） |

---

## 五、后端部署

| 状态 | 任务 | 说明 |
|:----:|------|------|
| ⬜ | 上传代码 | `backend/` 目录上传至服务器 |
| ⬜ | 创建虚拟环境 | `python3 -m venv venv` |
| ⬜ | 安装依赖 | `pip install -r requirements.txt`（遇 bcrypt 可装 `bcrypt<5.0`） |
| ⬜ | 进程管理 | systemd 或 supervisor 管理 uvicorn/gunicorn |
| ⬜ | 启动命令 | `uvicorn app.main:app --host 0.0.0.0 --port 8000` 或 gunicorn |

---

## 六、前端部署

| 状态 | 任务 | 说明 |
|:----:|------|------|
| ⬜ | 构建前端 | `VITE_API_BASE_URL=` 或 `VITE_API_BASE_URL=https://你的域名` 后 `npm run build` |
| ⬜ | 上传 dist | 将 `frontend/dist/` 上传至服务器（如 `/var/www/passgate/`） |
| ⬜ | 同域部署 | 前后端同域时可不设 VITE_API_BASE_URL，由 Nginx 代理 /api |

---

## 七、Nginx 配置

| 状态 | 任务 | 说明 |
|:----:|------|------|
| ⬜ | 静态文件 | root 指向 dist 目录，处理 SPA 路由（try_files） |
| ⬜ | 反向代理 /api | proxy_pass 到 localhost:8000 |
| ⬜ | 请求头 | 设置 Host、X-Forwarded-For、X-Forwarded-Proto |
| ⬜ | 超时 | proxy_read_timeout 等适当调大 |

---

## 八、HTTPS 与证书

| 状态 | 任务 | 说明 |
|:----:|------|------|
| ⬜ | 申请证书 | Let's Encrypt 或云厂商免费证书（微信 H5 扫码强制 HTTPS） |
| ⬜ | 配置 SSL | Nginx 监听 443，配置 ssl_certificate、ssl_certificate_key |
| ⬜ | HTTP 重定向 | 80 端口重定向到 443 |

---

## 九、Docker 化（可选）

| 状态 | 任务 | 说明 |
|:----:|------|------|
| ⬜ | Dockerfile 后端 | Python 基础镜像 + 依赖 + uvicorn |
| ⬜ | Dockerfile 前端 | nginx 镜像 + 构建产物 |
| ⬜ | docker-compose | 编排 backend、frontend、mysql（可选） |
| ⬜ | 环境变量注入 | 通过 env_file 或 environment 传入 |

---

## 十、上线验证

| 状态 | 任务 | 说明 |
|:----:|------|------|
| ⬜ | 登录测试 | https://域名 访问，admin/admin123 登录 |
| ⬜ | 出票流程 | 选电影、填手机号、生成二维码 |
| ⬜ | 检票流程 | 扫码核销（微信内需 HTTPS 才能用摄像头） |
| ⬜ | 修改默认密码 | 上线后立即修改 admin 密码 |

---

## 十一、运维与备份

| 状态 | 任务 | 说明 |
|:----:|------|------|
| ⬜ | 数据库备份 | 定期 mysqldump 或云 RDS 自动备份 |
| ⬜ | 日志目录 | 记录 Nginx、uvicorn 日志路径 |
| ⬜ | 监控告警 | 进程存活、磁盘、内存（可选） |

---

## 图例

- ⬜ 待完成
- 🔄 进行中
- ✅ 已完成

---

*部署完成后，可回填 [TODO.md](./TODO.md) 第七节对应项状态*
