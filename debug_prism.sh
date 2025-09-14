#!/bin/bash
# Debug Prism startup issues

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
export PRISM_ROOT="$SCRIPT_DIR/Prism"
export PRISM_LIBS="$PRISM_ROOT"

if [ ! -d "$PRISM_ROOT/PythonLibs" ]; then
    export PRISM_NO_LIBS="1"
fi

echo "=== Prism Debug Info ==="
echo "Python version: $(python3 --version)"
echo "PRISM_ROOT: $PRISM_ROOT"
echo "PRISM_LIBS: $PRISM_LIBS"
echo ""

# Try to import Qt first
echo "Testing Qt import..."
python3 -c "from qtpy.QtWidgets import QApplication; print('Qt import successful')" 2>&1

if [ $? -ne 0 ]; then
    echo "Qt import failed!"
    exit 1
fi

# Run with Python debugger
echo ""
echo "Starting Prism with Python debugger..."
echo "Type 'c' and press Enter to continue when you see the (Pdb) prompt"
echo ""
python3 -m pdb "$PRISM_ROOT/Scripts/PrismCore.py" "$@"