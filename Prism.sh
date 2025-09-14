#!/bin/bash
# Prism Pipeline - Linux Launcher

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Set Prism root directory
export PRISM_ROOT="$SCRIPT_DIR/Prism"

# Set Prism libs directory (required for libraries)
export PRISM_LIBS="$PRISM_ROOT"

# If libraries don't exist, allow running without them
if [ ! -d "$PRISM_ROOT/PythonLibs" ]; then
    export PRISM_NO_LIBS="1"
fi

# Launch Prism with Python 3
python3 "$PRISM_ROOT/Scripts/PrismCore.py" "$@"