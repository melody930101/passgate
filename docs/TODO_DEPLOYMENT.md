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
| ⬜ | 安装 Docker | `yum install docker` 或 `apt install docker.io`，并启用 `docker compose` |
| ⬜ | 安装 Nginx | 用于 HTTPS 终止与反向代理 |
| ⬜ | 设置时区 | 服务器 `TZ=Asia/Shanghai` 或 `timedatectl set-timezone Asia/Shanghai` |
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

## 四、数据库（云 MySQL）

| 状态 | 任务 | 说明 |
|:----:|------|------|
| ⬜ | 创建数据库 | `CREATE DATABASE passgate CHARACTER SET utf8mb4;` |
| ⬜ | 执行 init_db | `docker compose run --rm backend python -m scripts.init_db`，创建表 + 默认管理员 |
| ⬜ | 验证管理员 | 确认 `admin` / `admin123` 可登录（上线后改密） |

---

## 五、Docker 部署（推荐）

| 状态 | 任务 | 说明 |
|:----:|------|------|
| ⬜ | 安装 Docker | `yum install docker` / `apt install docker.io` + `docker compose` |
| ⬜ | 配置 backend/.env | DATABASE_URL 指向云 MySQL，SECRET_KEY、TIMEZONE 等 |
| ⬜ | 初始化数据库 | `docker compose run --rm backend python -m scripts.init_db` |
| ⬜ | 启动服务 | `docker compose up -d --build` |
| ⬜ | 验证 | backend:8000、frontend:8080 分别可访问 |

---

## 六、Nginx 配置

| 状态 | 任务 | 说明 |
|:----:|------|------|
| ⬜ | 复制配置 | 将 `docs/nginx-ai-melody.conf` 放入 `/etc/nginx/conf.d/passgate.conf` |
| ⬜ | 证书路径 | 确认 ssl_certificate、ssl_certificate_key 指向实际文件 |
| ⬜ | 重载 Nginx | `sudo nginx -t && sudo nginx -s reload` |

---

## 七、HTTPS 与证书

| 状态 | 任务 | 说明 |
|:----:|------|------|
| ⬜ | 申请证书 | Let's Encrypt 或云厂商免费证书（微信 H5 扫码强制 HTTPS） |
| ⬜ | 配置 SSL | Nginx 监听 443，配置 ssl_certificate、ssl_certificate_key |
| ⬜ | HTTP 重定向 | 80 端口重定向到 443 |

---

## 八、上线验证

| 状态 | 任务 | 说明 |
|:----:|------|------|
| ⬜ | 登录测试 | https://域名 访问，admin/admin123 登录 |
| ⬜ | 出票流程 | 选电影、填手机号、生成二维码 |
| ⬜ | 检票流程 | 扫码核销（微信内需 HTTPS 才能用摄像头） |
| ⬜ | 修改默认密码 | 上线后立即修改 admin 密码 |

---

## 九、运维与备份

| 状态 | 任务 | 说明 |
|:----:|------|------|
| ⬜ | 数据库备份 | 定期 mysqldump 或云 RDS 自动备份 |
| ⬜ | 日志目录 | 记录 Nginx、uvicorn 日志路径 |
| ⬜ | 监控告警 | 进程存活、磁盘、内存（可选） |

---

## 十、Git 拉取与一键部署

代码已推送到 [GitHub](https://github.com/melody930101/passgate.git)。

### 日常更新流程

```bash
cd /path/to/passgate
git pull
docker compose up -d --build
```

如需仅重启某一服务：`docker compose up -d --build backend` 或 `frontend`。

---

## 图例

- ⬜ 待完成
- 🔄 进行中
- ✅ 已完成

---

*部署完成后，可回填 [TODO.md](./TODO.md) 第七节对应项状态*
