#!/usr/bin/env python3
"""
Fix the Blender integration to set proper environment variables
"""

import os
import shutil

# Path to the installed PrismInit.py in Blender
blender_init_path = "/usr/share/blender/4.5/scripts/startup/PrismInit.py"

# Your Prism installation path
prism_path = "/home/lmarch/src/Prism/Prism"  # ADJUST THIS PATH

print("Fixing Blender Prism Integration")
print("=" * 50)

if not os.path.exists(blender_init_path):
    print(f"❌ Blender PrismInit.py not found at: {blender_init_path}")
    print("Integration may not be installed yet.")
    exit(1)

if not os.path.exists(prism_path):
    print(f"❌ Prism installation not found at: {prism_path}")
    print("Please adjust the prism_path variable in this script.")
    exit(1)

# Backup the original file
backup_path = blender_init_path + ".backup"
if not os.path.exists(backup_path):
    try:
        shutil.copy2(blender_init_path, backup_path)
        print(f"✓ Backed up original file to: {backup_path}")
    except Exception as e:
        print(f"❌ Failed to backup file: {e}")
        print("You may need to run this script with sudo")
        exit(1)

# Read the current file
try:
    with open(blender_init_path, 'r') as f:
        content = f.read()
    print("✓ Read current PrismInit.py")
except Exception as e:
    print(f"❌ Failed to read file: {e}")
    exit(1)

# Create the fixed content
fixed_content = f'''# -*- coding: utf-8 -*-
# Fixed Prism Integration for Linux

import os
import sys
import platform

# Set environment variables before importing anything else
os.environ["PRISM_ROOT"] = "{prism_path}"
os.environ["PRISM_LIBS"] = "{prism_path}"
os.environ["PRISM_NO_LIBS"] = "1"

# Add Prism to Python path
prism_scripts = os.path.join("{prism_path}", "Scripts")
if prism_scripts not in sys.path:
    sys.path.insert(0, prism_scripts)

# Now import Prism
try:
    import PrismCore
    print("Prism: Successfully initialized in Blender")
    
    # Initialize Prism for Blender
    pcore = PrismCore.PrismCore(app="Blender")
    
except Exception as e:
    print(f"Prism: Failed to initialize - {{e}}")
    import traceback
    traceback.print_exc()
'''

# Write the fixed file
try:
    with open(blender_init_path, 'w') as f:
        f.write(fixed_content)
    print("✓ Updated PrismInit.py with proper environment variables")
    print("\nNow try launching Blender normally:")
    print("blender")
except Exception as e:
    print(f"❌ Failed to write file: {e}")
    print("You may need to run this script with sudo:")
    print("sudo python3 fix_blender_integration.py")
    
    # Show what the user needs to do manually
    print("\n" + "="*50)
    print("MANUAL FIX:")
    print("="*50)
    print(f"1. Edit this file as root: {blender_init_path}")
    print("2. Replace the entire contents with:")
    print("-"*30)
    print(fixed_content)
    print("-"*30)