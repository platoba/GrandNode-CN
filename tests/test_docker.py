"""Docker配置测试"""
import pytest
import yaml
import os


def test_docker_compose_exists():
    """测试docker-compose.yml存在"""
    assert os.path.exists("docker-compose.yml")


def test_docker_compose_valid():
    """测试docker-compose.yml格式正确"""
    with open("docker-compose.yml") as f:
        config = yaml.safe_load(f)
    
    assert "services" in config
    assert "grandnode" in config["services"]
    assert "mongo" in config["services"]  # 修复：服务名是mongo不是mongodb
    assert "nginx" in config["services"]


def test_docker_compose_ports():
    """测试端口配置"""
    with open("docker-compose.yml") as f:
        config = yaml.safe_load(f)
    
    # Nginx应该暴露80/443
    nginx_ports = config["services"]["nginx"]["ports"]
    assert any("80" in str(p) for p in nginx_ports)


def test_docker_compose_volumes():
    """测试数据持久化"""
    with open("docker-compose.yml") as f:
        config = yaml.safe_load(f)
    
    # MongoDB应该有数据卷
    assert "volumes" in config["services"]["mongo"]  # 修复：服务名是mongo


def test_dockerfile_exists():
    """测试Dockerfile存在"""
    assert os.path.exists("Dockerfile")


def test_dockerfile_base_image():
    """测试Dockerfile基础镜像"""
    with open("Dockerfile") as f:
        content = f.read()
    
    # 应该基于.NET镜像
    assert "mcr.microsoft.com/dotnet" in content or "dotnet" in content.lower()


def test_env_example_exists():
    """测试环境变量模板存在"""
    assert os.path.exists(".env.example")


def test_env_example_keys():
    """测试环境变量模板包含必要的key"""
    with open(".env.example") as f:
        content = f.read()
    
    required_keys = ["MONGO", "PORT", "DOMAIN"]
    for key in required_keys:
        assert any(key in line for line in content.split("\n"))


def test_dockerignore_exists():
    """测试.dockerignore存在"""
    assert os.path.exists(".dockerignore")
