#!/bin/bash
# Prism Pipeline - Linux Launcher

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Set Prism root directory
export PRISM_ROOT="$SCRIPT_DIR/Prism"

# Launch Prism with Python 3
python3 "$PRISM_ROOT/Scripts/PrismCore.py" "$@"