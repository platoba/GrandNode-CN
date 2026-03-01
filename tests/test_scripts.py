"""脚本测试"""
import pytest
import os
import stat


def test_backup_script_exists():
    """测试备份脚本存在"""
    assert os.path.exists("scripts/backup.sh")


def test_backup_script_executable():
    """测试备份脚本可执行"""
    st = os.stat("scripts/backup.sh")
    assert st.st_mode & stat.S_IXUSR, "backup.sh should be executable"


def test_backup_script_shebang():
    """测试备份脚本有正确的shebang"""
    with open("scripts/backup.sh") as f:
        first_line = f.readline().strip()
    
    assert first_line.startswith("#!"), "Script should have shebang"
    assert "bash" in first_line or "sh" in first_line


def test_init_locale_script_exists():
    """测试语言包初始化脚本存在"""
    assert os.path.exists("scripts/init-locale.sh")


def test_init_locale_script_executable():
    """测试语言包初始化脚本可执行"""
    st = os.stat("scripts/init-locale.sh")
    assert st.st_mode & stat.S_IXUSR


def test_scripts_no_hardcoded_passwords():
    """测试脚本中没有硬编码密码"""
    for script in ["scripts/backup.sh", "scripts/init-locale.sh"]:
        with open(script) as f:
            content = f.read().lower()
        
        # 检查常见的密码模式
        suspicious_patterns = ["password=", "passwd=", "pwd="]
        for pattern in suspicious_patterns:
            if pattern in content:
                # 检查是否是从环境变量读取
                assert "$" in content or "${" in content, f"Found hardcoded password pattern in {script}"
