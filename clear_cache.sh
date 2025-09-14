#!/bin/bash
# Clear all Python cache files in Prism

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

echo "Clearing Python cache in $SCRIPT_DIR..."
find "$SCRIPT_DIR" -type f -name "*.pyc" -delete
find "$SCRIPT_DIR" -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
echo "Cache cleared!"