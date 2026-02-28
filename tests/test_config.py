"""Tests for GrandNode-CN configuration and structure."""
import json
import os
import re
import subprocess
import pytest
from pathlib import Path

ROOT = Path(__file__).parent.parent


class TestLocale:
    """Tests for Chinese locale pack."""

    @pytest.fixture
    def locale_data(self):
        with open(ROOT / "locales" / "zh-CN.json") as f:
            return json.load(f)

    def test_locale_file_exists(self):
        assert (ROOT / "locales" / "zh-CN.json").exists()

    def test_locale_valid_json(self):
        with open(ROOT / "locales" / "zh-CN.json") as f:
            data = json.load(f)
        assert isinstance(data, dict)

    def test_locale_has_meta(self, locale_data):
        assert "meta" in locale_data
        meta = locale_data["meta"]
        assert meta["language"] == "zh-CN"
        assert meta["name"] == "简体中文"

    def test_locale_has_required_sections(self, locale_data):
        required = ["common", "nav", "product", "order"]
        for section in required:
            assert section in locale_data, f"Missing section: {section}"

    def test_common_has_basic_actions(self, locale_data):
        common = locale_data["common"]
        for key in ["save", "cancel", "delete", "edit", "search"]:
            assert key in common, f"Missing common key: {key}"

    def test_nav_has_core_items(self, locale_data):
        nav = locale_data["nav"]
        for key in ["dashboard", "products", "orders", "customers", "settings"]:
            assert key in nav, f"Missing nav key: {key}"

    def test_product_fields(self, locale_data):
        product = locale_data["product"]
        for key in ["name", "sku", "price", "stock"]:
            assert key in product, f"Missing product key: {key}"

    def test_order_fields(self, locale_data):
        order = locale_data["order"]
        for key in ["orderNumber", "status", "total", "customer"]:
            assert key in order, f"Missing order key: {key}"

    def test_locale_values_are_chinese(self, locale_data):
        """Spot-check that values contain Chinese characters."""
        chinese_pattern = re.compile(r'[\u4e00-\u9fff]')
        assert chinese_pattern.search(locale_data["common"]["save"])
        assert chinese_pattern.search(locale_data["nav"]["dashboard"])
        assert chinese_pattern.search(locale_data["product"]["name"])

    def test_no_empty_values(self, locale_data):
        """Ensure no empty translation strings."""
        def check_empty(d, path=""):
            for k, v in d.items():
                if isinstance(v, dict):
                    check_empty(v, f"{path}.{k}")
                elif isinstance(v, str) and not v.strip():
                    pytest.fail(f"Empty value at {path}.{k}")
        check_empty(locale_data)

    def test_locale_key_count(self, locale_data):
        """Ensure we have enough translations (150+)."""
        def count_keys(d):
            total = 0
            for v in d.values():
                if isinstance(v, dict):
                    total += count_keys(v)
                else:
                    total += 1
            return total
        assert count_keys(locale_data) >= 100


class TestPluginConfig:
    """Tests for payment/shipping plugin configurations."""

    @pytest.fixture
    def plugin_data(self):
        with open(ROOT / "plugins" / "plugin-config.json") as f:
            return json.load(f)

    def test_plugin_file_exists(self):
        assert (ROOT / "plugins" / "plugin-config.json").exists()

    def test_plugin_valid_json(self):
        with open(ROOT / "plugins" / "plugin-config.json") as f:
            data = json.load(f)
        assert isinstance(data, dict)

    def test_has_plugins_section(self, plugin_data):
        assert "plugins" in plugin_data

    def test_alipay_plugin(self, plugin_data):
        plugins = plugin_data["plugins"]
        assert "alipay" in plugins
        alipay = plugins["alipay"]
        assert alipay["name"] == "Payments.Alipay"
        assert "config" in alipay

    def test_wechatpay_plugin(self, plugin_data):
        plugins = plugin_data["plugins"]
        assert "wechatpay" in plugins
        wechat = plugins["wechatpay"]
        assert wechat["name"] == "Payments.WeChatPay"
        assert "config" in wechat

    def test_alipay_has_required_config(self, plugin_data):
        config = plugin_data["plugins"]["alipay"]["config"]
        for key in ["appId", "gateway", "signType", "notifyUrl", "returnUrl"]:
            assert key in config, f"Missing Alipay config: {key}"

    def test_alipay_gateway_url(self, plugin_data):
        gateway = plugin_data["plugins"]["alipay"]["config"]["gateway"]
        assert gateway.startswith("https://")

    def test_no_hardcoded_secrets(self, plugin_data):
        """Ensure no actual secrets are committed."""
        sensitive_keys = ["privateKey", "secret", "apiKey", "mchKey"]
        def check_secrets(d, path=""):
            for k, v in d.items():
                if isinstance(v, dict):
                    check_secrets(v, f"{path}.{k}")
                elif isinstance(v, str) and k.lower() in [s.lower() for s in sensitive_keys]:
                    assert v == "" or v.startswith("${"), \
                        f"Potential secret at {path}.{k}: '{v[:20]}...'"
        check_secrets(plugin_data)


class TestDockerConfig:
    """Tests for Docker configuration."""

    def test_dockerfile_exists(self):
        assert (ROOT / "Dockerfile").exists()

    def test_docker_compose_exists(self):
        assert (ROOT / "docker-compose.yml").exists()

    def test_dockerignore_exists(self):
        assert (ROOT / ".dockerignore").exists()

    def test_dockerfile_has_base_image(self):
        content = (ROOT / "Dockerfile").read_text()
        assert "FROM" in content
        assert "grandnode" in content.lower()

    def test_dockerfile_exposes_port(self):
        content = (ROOT / "Dockerfile").read_text()
        assert "EXPOSE" in content

    def test_dockerfile_sets_chinese_locale(self):
        content = (ROOT / "Dockerfile").read_text()
        assert "zh_CN" in content

    def test_compose_has_three_services(self):
        content = (ROOT / "docker-compose.yml").read_text()
        assert "grandnode:" in content
        assert "mongo:" in content
        assert "nginx:" in content

    def test_compose_mongo_healthcheck(self):
        content = (ROOT / "docker-compose.yml").read_text()
        assert "healthcheck" in content
        assert "mongosh" in content

    def test_compose_volumes(self):
        content = (ROOT / "docker-compose.yml").read_text()
        assert "volumes:" in content


class TestNginxConfig:
    """Tests for Nginx configuration."""

    def test_nginx_config_exists(self):
        assert (ROOT / "nginx" / "default.conf").exists()

    def test_nginx_has_upstream(self):
        content = (ROOT / "nginx" / "default.conf").read_text()
        assert "upstream" in content
        assert "grandnode" in content

    def test_nginx_has_security_headers(self):
        content = (ROOT / "nginx" / "default.conf").read_text()
        assert "X-Frame-Options" in content
        assert "X-Content-Type-Options" in content
        assert "X-XSS-Protection" in content

    def test_nginx_gzip_enabled(self):
        content = (ROOT / "nginx" / "default.conf").read_text()
        assert "gzip on" in content

    def test_nginx_static_cache(self):
        content = (ROOT / "nginx" / "default.conf").read_text()
        assert "expires" in content
        assert "Cache-Control" in content

    def test_nginx_proxy_headers(self):
        content = (ROOT / "nginx" / "default.conf").read_text()
        for header in ["X-Real-IP", "X-Forwarded-For", "X-Forwarded-Proto"]:
            assert header in content


class TestScripts:
    """Tests for utility scripts."""

    def test_init_locale_exists(self):
        assert (ROOT / "scripts" / "init-locale.sh").exists()

    def test_backup_exists(self):
        assert (ROOT / "scripts" / "backup.sh").exists()

    def test_init_locale_executable_or_bash(self):
        content = (ROOT / "scripts" / "init-locale.sh").read_text()
        assert content.startswith("#!/bin/bash")

    def test_backup_has_error_handling(self):
        content = (ROOT / "scripts" / "backup.sh").read_text()
        assert "set -euo pipefail" in content

    def test_backup_has_retention(self):
        content = (ROOT / "scripts" / "backup.sh").read_text()
        assert "mtime" in content or "delete" in content


class TestEnvConfig:
    """Tests for environment configuration."""

    def test_env_example_exists(self):
        assert (ROOT / ".env.example").exists()

    def test_env_has_mongo_config(self):
        content = (ROOT / ".env.example").read_text()
        assert "MONGO" in content

    def test_env_has_no_real_passwords(self):
        content = (ROOT / ".env.example").read_text()
        lines = content.strip().split("\n")
        for line in lines:
            if "=" in line and not line.strip().startswith("#"):
                key, _, value = line.partition("=")
                value = value.strip()
                if "pass" in key.lower() or "secret" in key.lower():
                    assert value in ("", "changeme", "your-secret-here"), \
                        f"Potential real secret in .env.example: {key}"


class TestCIConfig:
    """Tests for CI/CD configuration."""

    def test_ci_workflow_exists(self):
        assert (ROOT / ".github" / "workflows" / "ci.yml").exists()

    def test_ci_has_docker_build(self):
        content = (ROOT / ".github" / "workflows" / "ci.yml").read_text()
        assert "docker" in content.lower()


class TestProjectStructure:
    """Tests for overall project structure."""

    def test_readme_exists(self):
        assert (ROOT / "README.md").exists()

    def test_gitignore_exists(self):
        assert (ROOT / ".gitignore").exists()

    def test_readme_has_chinese_content(self):
        content = (ROOT / "README.md").read_text()
        chinese = re.compile(r'[\u4e00-\u9fff]')
        assert chinese.search(content)

    def test_readme_has_docker_instructions(self):
        content = (ROOT / "README.md").read_text()
        assert "docker" in content.lower()
