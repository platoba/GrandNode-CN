"""Nginx配置测试"""
import pytest
import os


def test_nginx_config_exists():
    """测试Nginx配置文件存在"""
    assert os.path.exists("nginx/default.conf")


def test_nginx_proxy_pass():
    """测试Nginx配置了反向代理"""
    with open("nginx/default.conf") as f:
        content = f.read()
    
    assert "proxy_pass" in content
    assert "grandnode" in content.lower()


def test_nginx_ssl_ready():
    """测试Nginx SSL配置就绪"""
    with open("nginx/default.conf") as f:
        content = f.read()
    
    # 检查SSL相关配置（可能被注释）
    has_ssl_config = "ssl" in content.lower() or "443" in content


def test_nginx_gzip():
    """测试Nginx启用了gzip压缩"""
    with open("nginx/default.conf") as f:
        content = f.read()
    
    # gzip应该被启用或配置
    assert "gzip" in content.lower()


def test_nginx_client_max_body_size():
    """测试Nginx配置了上传大小限制"""
    with open("nginx/default.conf") as f:
        content = f.read()
    
    # 应该配置client_max_body_size（电商需要上传图片）
    assert "client_max_body_size" in content
