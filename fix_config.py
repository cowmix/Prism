#!/usr/bin/env python3
"""
Fix Prism config to prevent segfault on startup
"""

import json
import os
import shutil
from pathlib import Path

config_path = Path.home() / ".config" / "Prism" / "Prism.json"

if not config_path.exists():
    print(f"Config file not found at {config_path}")
    exit(1)

# Backup the config
backup_path = config_path.with_suffix('.json.backup')
shutil.copy2(config_path, backup_path)
print(f"Backed up config to {backup_path}")

# Load and fix the config
with open(config_path, 'r') as f:
    config = json.load(f)

# Clear the current project
if 'globals' in config and 'current project' in config['globals']:
    print(f"Current project was: {config['globals']['current project']}")
    config['globals']['current project'] = ""
    print("Cleared current project")

# Save the fixed config
with open(config_path, 'w') as f:
    json.dump(config, f, indent=4)

print(f"Config fixed! Try running Prism again.")
print("\nNote: The project still exists and can be loaded manually after Prism starts.")