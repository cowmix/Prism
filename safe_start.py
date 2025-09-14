#!/usr/bin/env python3
"""
Safe startup script for Prism - minimal initialization
"""

import os
import sys
import traceback

# Set up paths
script_dir = os.path.dirname(os.path.abspath(__file__))
prism_root = os.path.join(script_dir, "Prism")
sys.path.insert(0, os.path.join(prism_root, "Scripts"))

os.environ["PRISM_ROOT"] = prism_root
os.environ["PRISM_LIBS"] = prism_root
os.environ["PRISM_NO_LIBS"] = "1"

print("Starting Prism in safe mode...")
print(f"Prism root: {prism_root}")

try:
    # Try to import PrismCore
    import PrismCore
    
    # Create core instance with minimal settings
    core = PrismCore.PrismCore(app="Standalone")
    
    # Check if there's a project
    if core.getConfig("globals", "current project"):
        print(f"Current project: {core.getConfig('globals', 'current project')}")
    
    # Try to start the project browser
    print("Starting Project Browser...")
    core.projects.setProject(openUi="projectBrowser")
    
    # Start Qt event loop
    from qtpy.QtWidgets import QApplication
    import sys
    
    if not QApplication.instance():
        app = QApplication(sys.argv)
    else:
        app = QApplication.instance()
    
    sys.exit(app.exec_())
    
except Exception as e:
    print(f"Error starting Prism: {e}")
    traceback.print_exc()
    
    # Try to clear any problematic settings
    print("\nTrying to reset configuration...")
    config_path = os.path.expanduser("~/.config/Prism/Prism.yml")
    if os.path.exists(config_path):
        backup_path = config_path + ".backup"
        print(f"Backing up config to {backup_path}")
        import shutil
        shutil.copy2(config_path, backup_path)
        
        # Try to fix the config
        try:
            import ruamel.yaml
            yaml = ruamel.yaml.YAML()
            with open(config_path, 'r') as f:
                config = yaml.load(f)
            
            # Remove potentially problematic settings
            if 'globals' in config and 'current project' in config['globals']:
                print("Clearing current project setting...")
                config['globals']['current project'] = ""
            
            with open(config_path, 'w') as f:
                yaml.dump(config, f)
            
            print("Config reset. Try running Prism again.")
        except:
            print("Could not reset config automatically.")
            print(f"You can manually restore from backup: {backup_path}")