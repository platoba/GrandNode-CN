#!/usr/bin/env python3
"""Health check for GrandNode-CN deployment."""
import json
import sys
from pathlib import Path


def check_locale():
    """Verify Chinese locale file integrity."""
    locale_file = Path("locales/zh-CN.json")
    if not locale_file.exists():
        return False, "zh-CN.json not found"
    try:
        data = json.loads(locale_file.read_text())
        sections = ["meta", "common", "nav", "product", "order"]
        missing = [s for s in sections if s not in data]
        if missing:
            return False, f"Missing sections: {missing}"
        return True, f"OK ({sum(1 for _ in _flatten_keys(data))} keys)"
    except json.JSONDecodeError as e:
        return False, f"Invalid JSON: {e}"


def check_plugins():
    """Verify plugin config."""
    plugin_file = Path("plugins/plugin-config.json")
    if not plugin_file.exists():
        return False, "plugin-config.json not found"
    try:
        data = json.loads(plugin_file.read_text())
        plugins = data.get("plugins", {})
        return True, f"OK ({len(plugins)} plugins: {', '.join(plugins.keys())})"
    except json.JSONDecodeError as e:
        return False, f"Invalid JSON: {e}"


def check_docker():
    """Verify Docker files."""
    issues = []
    if not Path("Dockerfile").exists():
        issues.append("Dockerfile missing")
    if not Path("docker-compose.yml").exists():
        issues.append("docker-compose.yml missing")
    if not Path("nginx/default.conf").exists():
        issues.append("nginx config missing")
    return (len(issues) == 0, "OK" if not issues else "; ".join(issues))


def check_scripts():
    """Verify scripts."""
    scripts = ["scripts/init-locale.sh", "scripts/backup.sh"]
    missing = [s for s in scripts if not Path(s).exists()]
    return (len(missing) == 0, "OK" if not missing else f"Missing: {missing}")


def _flatten_keys(d, prefix=""):
    for k, v in d.items():
        if isinstance(v, dict):
            yield from _flatten_keys(v, f"{prefix}{k}.")
        else:
            yield f"{prefix}{k}"


def main():
    checks = {
        "Locale": check_locale,
        "Plugins": check_plugins,
        "Docker": check_docker,
        "Scripts": check_scripts,
    }

    all_ok = True
    for name, fn in checks.items():
        ok, msg = fn()
        status = "✅" if ok else "❌"
        print(f"  {status} {name}: {msg}")
        if not ok:
            all_ok = False

    sys.exit(0 if all_ok else 1)


if __name__ == "__main__":
    main()
