.PHONY: help build up down logs test monitor backup clean

help:
	@echo "GrandNode-CN Makefile"
	@echo "====================="
	@echo "make build    - 构建Docker镜像"
	@echo "make up       - 启动服务"
	@echo "make down     - 停止服务"
	@echo "make logs     - 查看日志"
	@echo "make test     - 运行测试"
	@echo "make monitor  - 性能监控"
	@echo "make backup   - 备份数据库"
	@echo "make clean    - 清理容器和数据"

build:
	docker compose build

up:
	docker compose up -d
	@echo "✓ GrandNode started at http://localhost:8080"

down:
	docker compose down

logs:
	docker compose logs -f

test:
	pytest tests/ -v

monitor:
	python scripts/monitor.py http://localhost:8080

backup:
	./scripts/backup.sh

clean:
	docker compose down -v
	rm -f *.log monitor-report.json
