#!/bin/bash
# Launch Blender with Prism environment variables

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Set Prism environment variables
export PRISM_ROOT="$SCRIPT_DIR/Prism"
export PRISM_LIBS="$PRISM_ROOT"
export PRISM_NO_LIBS="1"

echo "Starting Blender with Prism..."
echo "PRISM_ROOT: $PRISM_ROOT"
echo "PRISM_LIBS: $PRISM_LIBS"

# Launch Blender
blender "$@"