#!/bin/bash
# Initialize Chinese locale for GrandNode
set -euo pipefail

echo "Initializing Chinese (zh-CN) locale for GrandNode..."

# The locale JSON is already copied via Dockerfile
# This script handles any runtime initialization

LOCALE_DIR="/app/App_Data/Localization"

if [ -f "$LOCALE_DIR/zh-CN.json" ]; then
    echo "✅ Chinese locale file found"
else
    echo "⚠️  Chinese locale file missing, creating default..."
    cp "$LOCALE_DIR/en.json" "$LOCALE_DIR/zh-CN.json" 2>/dev/null || true
fi

echo "Locale initialization complete."
