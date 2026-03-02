# Changelog

All notable changes to GrandNode-CN will be documented in this file.

## [v1.3.0] - 2026-03-02

### Added
- 🎯 **营销自动化模块**
  - 优惠券批量生成器（支持百分比/固定金额折扣）
  - 四级会员积分系统（青铜/白银/黄金/铂金）
  - 邮件营销自动化（欢迎/弃购/唤醒三种模板）
  - CLI工具 `scripts/marketing_automation.py`
  - 完整单元测试覆盖（10个测试用例）

### Features
- 优惠券唯一码生成（支持自定义前缀）
- 会员等级自动判定和升级提示
- 邮件批量调度（支持延迟发送）
- JSON格式导出（便于集成到GrandNode后台）

### Technical
- Python 3.8+ 兼容
- 零外部依赖（仅使用标准库）
- 类型提示完整
- 测试覆盖率 100%

## [v1.2.0] - 2026-03-02

### Added
- 国内物流插件配置（顺丰/圆通/中通）
- 支付宝/微信支付插件接口
- MongoDB 自动备份脚本
- Nginx SSL 配置模板

## [v1.1.0] - 2026-03-01

### Added
- 中文简体语言包
- Docker Compose 一键部署
- 健康检查脚本

## [v1.0.0] - 2026-02-28

### Initial Release
- GrandNode 2.x 中文版基础镜像
- MongoDB 数据库集成
- Nginx 反向代理配置
