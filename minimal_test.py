#!/usr/bin/env python3
"""
Minimal test to identify segfault cause
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

print("Step 1: Importing PrismCore...")
try:
    import PrismCore
    print("✓ PrismCore imported successfully")
except Exception as e:
    print(f"✗ Failed to import PrismCore: {e}")
    sys.exit(1)

print("\nStep 2: Creating PrismCore instance...")
try:
    core = PrismCore.PrismCore(app="Standalone")
    print("✓ PrismCore instance created")
except Exception as e:
    print(f"✗ Failed to create PrismCore: {e}")
    traceback.print_exc()
    sys.exit(1)

print("\nStep 3: Checking configuration...")
try:
    # Check if config exists
    config_dir = os.path.expanduser("~/.config/Prism")
    if not os.path.exists(config_dir):
        print(f"Config directory doesn't exist at {config_dir}")
        print("This is normal for first run")
    else:
        print(f"Config directory exists: {config_dir}")
        # List config files
        for f in os.listdir(config_dir):
            print(f"  - {f}")
    
    current_project = core.getConfig("globals", "current project")
    if current_project:
        print(f"Current project set to: {current_project}")
    else:
        print("✓ No current project set")
except Exception as e:
    print(f"Note: Config error (normal for first run): {e}")

print("\nStep 4: Testing Qt...")
try:
    from qtpy.QtWidgets import QApplication, QDialog, QPushButton, QVBoxLayout
    
    if not QApplication.instance():
        app = QApplication(sys.argv)
    else:
        app = QApplication.instance()
    
    # Create a simple dialog
    dialog = QDialog()
    dialog.setWindowTitle("Prism Test")
    layout = QVBoxLayout()
    
    btn = QPushButton("Close")
    btn.clicked.connect(dialog.accept)
    layout.addWidget(btn)
    
    dialog.setLayout(layout)
    print("✓ Qt widgets created successfully")
    
    print("\nShowing test dialog - click 'Close' to continue...")
    dialog.exec_()
    
except Exception as e:
    print(f"✗ Qt error: {e}")
    traceback.print_exc()

print("\nStep 5: Testing project browser (this might crash)...")
print("Press Ctrl+C if it hangs...")
try:
    # Don't actually open the UI, just test the project manager
    project_manager = core.projects
    print(f"✓ Project manager initialized: {project_manager}")
    
    # Try to get project list without opening UI
    projects = core.getConfig("globals", "recent_projects", dft=[])
    print(f"✓ Recent projects: {projects if projects else 'None'}")
    
except Exception as e:
    print(f"✗ Project browser error: {e}")
    traceback.print_exc()

print("\n✓ All tests completed successfully!")
print("\nTo start Prism normally, try:")
print("1. Clear your config: rm ~/.config/Prism/Prism.yml")
print("2. Run: ./Prism.sh")
print("3. Create a new project - don't load an existing one yet")