# Changelog

All notable changes to GrandNode-CN will be documented in this file.

## [2.0.0] - 2026-03-02

### Added
- 完整pytest测试套件（48个测试）
  - Docker配置测试（10个）
  - 中文语言包测试（5个）
  - 脚本测试（6个）
  - Nginx配置测试（5个）
  - 插件测试（3个）
  - 原有配置测试（2个）
- 性能监控工具 `scripts/monitor.py`
  - 健康检查
  - 首页响应时间
  - API端点监控
  - JSON报告导出
- 健康检查脚本 `scripts/healthcheck.sh`（Docker HEALTHCHECK）
- 日志分析工具 `scripts/analyze-logs.py`
  - 错误统计
  - HTTP请求分析
  - 慢查询检测
- GitHub Actions CI/CD增强
  - 测试覆盖率报告
  - Docker镜像构建测试
  - Trivy安全扫描
  - 脚本语法检查
- Makefile运维工具（8个命令）
- CHANGELOG版本记录

### Changed
- CI workflow增强（3个job: test/docker/security）
- README更新（添加监控和日志分析说明）

### Fixed
- 无

## [1.0.0] - 2026-02-27

### Added
- 初始版本
- Docker Compose一键部署
- 中文语言包
- 支付宝/微信支付插件接口
- MongoDB备份脚本
- Nginx反向代理配置
