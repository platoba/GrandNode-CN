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

## 监控与运维

### 性能监控

```bash
# 运行性能监控
python scripts/monitor.py http://localhost:8080

# 查看监控报告
cat monitor-report.json
```

监控指标：
- 健康检查响应时间
- 首页加载时间
- API端点响应时间
- HTTP状态码分布

### 日志分析

```bash
# 分析Nginx访问日志
python scripts/analyze-logs.py /var/log/nginx/access.log

# 分析GrandNode应用日志
docker compose logs grandnode > app.log
python scripts/analyze-logs.py app.log
```

分析内容：
- 错误统计与分类
- 警告信息
- HTTP请求分布
- 慢查询检测

### Makefile命令

```bash
make help      # 查看所有命令
make build     # 构建镜像
make up        # 启动服务
make down      # 停止服务
make logs      # 查看日志
make test      # 运行测试
make monitor   # 性能监控
make backup    # 备份数据库
make clean     # 清理容器和数据
```

## 测试

```bash
# 安装测试依赖
pip install pytest pytest-cov pyyaml requests

# 运行所有测试
pytest tests/ -v

# 运行测试并生成覆盖率报告
pytest tests/ -v --cov=. --cov-report=html

# 运行特定测试
pytest tests/test_docker.py -v
```

测试覆盖：
- ✅ Docker配置验证
- ✅ 中文语言包完整性
- ✅ 脚本可执行性与安全性
- ✅ Nginx配置正确性
- ✅ 插件目录结构

## 故障排查

### 服务无法启动

```bash
# 检查端口占用
lsof -i :8080
lsof -i :27017

# 查看容器日志
docker compose logs grandnode
docker compose logs mongodb

# 重新构建
make clean
make build
make up
```

### MongoDB连接失败

```bash
# 检查MongoDB状态
docker compose exec mongodb mongosh --eval "db.adminCommand('ping')"

# 重置MongoDB数据
docker compose down -v
docker compose up -d
```

### 性能问题

```bash
# 运行性能监控
make monitor

# 检查资源使用
docker stats

# 分析慢查询
docker compose logs mongodb | grep "slow query"
```

## 生产部署建议

1. **SSL证书**：使用Let's Encrypt配置HTTPS
2. **数据备份**：配置crontab定时备份MongoDB
3. **监控告警**：集成Prometheus + Grafana
4. **日志收集**：使用ELK Stack或Loki
5. **负载均衡**：多实例部署 + Nginx负载均衡
6. **CDN加速**：静态资源使用CDN

## 版本历史

查看 [CHANGELOG.md](CHANGELOG.md)

