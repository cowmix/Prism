#!/bin/bash
# Prism Safe Mode - Starts without auto-loading projects

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
export PRISM_ROOT="$SCRIPT_DIR/Prism"
export PRISM_LIBS="$PRISM_ROOT"

if [ ! -d "$PRISM_ROOT/PythonLibs" ]; then
    export PRISM_NO_LIBS="1"
fi

# Backup current config
CONFIG_FILE="$HOME/.config/Prism/Prism.json"
if [ -f "$CONFIG_FILE" ]; then
    cp "$CONFIG_FILE" "$CONFIG_FILE.temp_backup"
    
    # Clear current project using Python
    python3 -c "
import json
config_file = '$CONFIG_FILE'
with open(config_file, 'r') as f:
    config = json.load(f)
if 'globals' in config:
    config['globals']['current project'] = ''
with open(config_file, 'w') as f:
    json.dump(config, f, indent=4)
print('Cleared current project from config')
"
fi

echo "Starting Prism in safe mode (no auto-load)..."
python3 "$PRISM_ROOT/Scripts/PrismCore.py" "$@"

# Restore config after Prism closes
if [ -f "$CONFIG_FILE.temp_backup" ]; then
    mv "$CONFIG_FILE.temp_backup" "$CONFIG_FILE"
fi