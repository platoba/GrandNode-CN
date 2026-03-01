"""中文语言包测试"""
import pytest
import json
import os


def test_locale_file_exists():
    """测试中文语言包存在"""
    assert os.path.exists("locales/zh-CN.json")


def test_locale_valid_json():
    """测试语言包JSON格式正确"""
    with open("locales/zh-CN.json") as f:
        data = json.load(f)
    
    assert isinstance(data, dict)
    assert len(data) > 0


def test_locale_common_keys():
    """测试常用翻译key存在"""
    with open("locales/zh-CN.json") as f:
        data = json.load(f)
    
    # 检查常见电商术语
    common_terms = ["product", "cart", "checkout", "order", "payment"]
    found_count = sum(1 for term in common_terms if any(term in k.lower() for k in data.keys()))
    
    # 至少应该有一些常见术语
    assert found_count > 0


def test_locale_no_empty_values():
    """测试语言包没有空值"""
    with open("locales/zh-CN.json") as f:
        data = json.load(f)
    
    empty_values = [k for k, v in data.items() if not v or (isinstance(v, str) and not v.strip())]
    assert len(empty_values) == 0, f"Found empty values: {empty_values}"


def test_locale_chinese_characters():
    """测试语言包包含中文字符"""
    with open("locales/zh-CN.json") as f:
        content = f.read()
    
    # 检查是否包含中文字符（Unicode范围）
    has_chinese = any('\u4e00' <= char <= '\u9fff' for char in content)
    assert has_chinese, "Language pack should contain Chinese characters"
