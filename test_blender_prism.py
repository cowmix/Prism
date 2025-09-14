"""
Test script to run inside Blender's Text Editor
Paste this into Blender's Text Editor and click "Run Script"
"""

import os
import sys
import bpy

print("=" * 50)
print("BLENDER PRISM DEBUG")
print("=" * 50)

# Check environment variables
print("1. Environment Variables:")
prism_vars = ["PRISM_ROOT", "PRISM_LIBS", "PRISM_APP_PLUGIN_ROOT"]
for var in prism_vars:
    value = os.environ.get(var, "NOT SET")
    print(f"   {var}: {value}")

print("\n2. Python Path:")
for i, path in enumerate(sys.path[:5]):  # Show first 5 paths
    print(f"   {i}: {path}")

print("\n3. Blender Add-ons:")
addon_names = [name for name in bpy.context.preferences.addons.keys() if "prism" in name.lower()]
print(f"   Prism-related addons: {addon_names}")

print("\n4. Blender Scripts/Startup:")
startup_path = bpy.utils.user_resource('SCRIPTS', path="startup")
print(f"   Startup path: {startup_path}")
if os.path.exists(startup_path):
    startup_files = [f for f in os.listdir(startup_path) if "prism" in f.lower()]
    print(f"   Prism files in startup: {startup_files}")

print("\n5. Test Prism Import:")
try:
    # Set up paths manually
    script_dir = "/home/lmarch/src/Prism"  # ADJUST THIS PATH
    prism_root = script_dir + "/Prism"
    
    if prism_root not in sys.path:
        sys.path.insert(0, prism_root + "/Scripts")
    
    os.environ["PRISM_ROOT"] = prism_root
    os.environ["PRISM_LIBS"] = prism_root
    os.environ["PRISM_NO_LIBS"] = "1"
    
    import PrismCore
    print("   ✓ PrismCore imported successfully!")
    
    # Try to create a Prism instance
    core = PrismCore.PrismCore(app="Blender")
    print("   ✓ PrismCore instance created!")
    
    print(f"   Prism version: {core.version}")
    
except Exception as e:
    print(f"   ✗ Failed to import/create PrismCore: {e}")
    import traceback
    traceback.print_exc()

print("\n6. Check Blender UI:")
# Check if Prism menu exists
context = bpy.context
if hasattr(context, 'window_manager'):
    wm = context.window_manager
    print(f"   Window manager available: {wm}")

print("\n" + "=" * 50)
print("Copy this output and let me know what you see!")
print("=" * 50)