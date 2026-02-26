# Stage 1: Build
FROM node:20-alpine AS builder

WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Stage 2: Serve with nginx
FROM nginx:alpine

# 在容器内将构建产物放在 /usr/share/nginx/html/passgate，以匹配 base: '/passgate/'
COPY --from=builder /app/dist /usr/share/nginx/html/passgate
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
