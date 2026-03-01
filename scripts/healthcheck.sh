#!/bin/bash
# GrandNode健康检查脚本（用于Docker HEALTHCHECK）

set -e

# 检查GrandNode服务
if curl -f http://localhost:5000/health > /dev/null 2>&1; then
    echo "✓ GrandNode is healthy"
    exit 0
else
    echo "✗ GrandNode is unhealthy"
    exit 1
fi
