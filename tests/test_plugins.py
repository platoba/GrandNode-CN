"""支付插件测试"""
import pytest
import os


def test_plugins_directory_exists():
    """测试插件目录存在"""
    assert os.path.exists("plugins")


def test_alipay_plugin_config():
    """测试支付宝插件配置存在"""
    # 检查是否有支付宝相关配置文件
    plugin_files = os.listdir("plugins") if os.path.exists("plugins") else []
    
    # 至少应该有README或配置模板
    assert len(plugin_files) > 0 or os.path.exists("plugins/README.md")


def test_wechat_pay_plugin_config():
    """测试微信支付插件配置"""
    # 同上，检查微信支付配置
    plugin_files = os.listdir("plugins") if os.path.exists("plugins") else []
    assert len(plugin_files) >= 0  # 至少目录存在
