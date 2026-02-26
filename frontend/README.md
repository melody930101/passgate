# Passgate Frontend

Vue 3 前端，票务系统工作人员端 H5。

## 快速开始

```bash
# 安装依赖
npm install

# 开发（需先启动后端，默认代理到 localhost:8000）
npm run dev

# 构建
npm run build
```

## 环境变量

- `VITE_API_BASE_URL`: 后端地址，不设则使用相对路径 /api（配合 Vite 代理）
