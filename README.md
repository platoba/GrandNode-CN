# GrandNode-CN 🇨🇳

GrandNode 中文版 Docker 一键部署。基于 [GrandNode](https://github.com/grandnode/grandnode2) 开源电商平台，预配置中文语言包、支付宝/微信支付插件接口、国内镜像加速。

## 特性

- 🐳 Docker Compose 一键启动（GrandNode + MongoDB + Nginx）
- 🇨🇳 预装中文简体语言包
- 💰 支付宝/微信支付插件接口预留
- 📦 国内物流对接（顺丰/圆通/中通 API 接口）
- 🔧 生产级 Nginx 反向代理 + SSL
- 📊 MongoDB 数据备份脚本

## 快速开始

```bash
git clone https://github.com/platoba/GrandNode-CN.git
cd GrandNode-CN
cp .env.example .env
docker compose up -d
# 访问 http://localhost:8080 完成安装向导
```

## 架构

```
┌─────────────┐     ┌──────────────┐     ┌──────────────┐
│   Nginx     │────▶│  GrandNode   │────▶│   MongoDB    │
│  (反向代理)  │     │  (.NET 8)    │     │   (数据库)    │
└─────────────┘     └──────────────┘     └──────────────┘
      :443                :5000               :27017
```

## 目录结构

```
├── docker-compose.yml    # 编排文件
├── Dockerfile            # GrandNode 中文定制镜像
├── nginx/                # Nginx 配置
│   └── default.conf
├── scripts/
│   ├── backup.sh         # MongoDB 备份
│   └── init-locale.sh    # 中文语言包初始化
├── locales/
│   └── zh-CN.json        # 中文翻译
└── .env.example          # 环境变量模板
```

## 配置

编辑 `.env` 文件：

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `GRANDNODE_PORT` | 对外端口 | 8080 |
| `MONGO_ROOT_USER` | MongoDB 用户 | admin |
| `MONGO_ROOT_PASS` | MongoDB 密码 | changeme |
| `DOMAIN` | 域名（SSL用） | localhost |

## 支付集成

支付宝和微信支付通过 GrandNode 插件系统集成。配置文件位于 `plugins/` 目录。

## 备份

```bash
# 手动备份
./scripts/backup.sh

# 自动备份（crontab）
0 2 * * * /path/to/GrandNode-CN/scripts/backup.sh
```

## License

MIT（GrandNode 本身为 GPL-3.0）
