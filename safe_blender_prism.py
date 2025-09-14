#!/usr/bin/env python3
"""
Create a patched PrismInit.py that prevents crashes in Blender
"""

import os
import shutil

# Your Prism installation path
prism_path = "/home/lmarch/src/Prism/Prism"  # ADJUST THIS PATH

# Create a safe PrismInit.py content that avoids crashes
safe_content = f'''# -*- coding: utf-8 -*-
# Safe Prism Integration for Blender - Prevents crashes

import os
import sys
import platform

# Set environment variables
os.environ["PRISM_ROOT"] = "{prism_path}"
os.environ["PRISM_LIBS"] = "{prism_path}"
os.environ["PRISM_NO_LIBS"] = "1"

# Add Prism to Python path
prism_scripts = os.path.join("{prism_path}", "Scripts")
if prism_scripts not in sys.path:
    sys.path.insert(0, prism_scripts)

try:
    import PrismCore
    import bpy
    from bpy.types import Menu, Operator
    from bpy.props import StringProperty
    
    print("Prism: Safe mode initialization...")
    
    # Create a safe Prism core instance (no project loading)
    pcore = PrismCore.PrismCore(app="Blender")
    
    # Clear any auto-loading project to prevent crashes
    if pcore.getConfig("globals", "current project"):
        print("Prism: Clearing auto-load project to prevent crashes")
        pcore.setConfig("globals", "current project", "")
    
    # Safe Prism menu operators (these shouldn't crash)
    class PRISM_OT_safe_project_browser(Operator):
        """Open Project Browser (Safe)"""
        bl_idname = "prism.safe_project_browser"
        bl_label = "Project Browser (Safe)"
        
        def execute(self, context):
            try:
                # Don't auto-load any project
                pcore.projects.setProject(openUi="projectBrowser")
                return {{'FINISHED'}}
            except Exception as e:
                self.report({{'ERROR'}}, f"Failed to open Project Browser: {{e}}")
                return {{'CANCELLED'}}
    
    class PRISM_OT_safe_settings(Operator):
        """Open Prism Settings (Safe)"""
        bl_idname = "prism.safe_settings"
        bl_label = "Settings (Safe)"
        
        def execute(self, context):
            try:
                pcore.prismSettings()
                return {{'FINISHED'}}
            except Exception as e:
                self.report({{'ERROR'}}, f"Failed to open Settings: {{e}}")
                return {{'CANCELLED'}}
    
    class PRISM_OT_about(Operator):
        """About Prism"""
        bl_idname = "prism.about"
        bl_label = "About"
        
        def execute(self, context):
            self.report({{'INFO'}}, f"Prism {{pcore.version}} - Linux port by Claude")
            return {{'FINISHED'}}
    
    # Safe Prism menu
    class TOPBAR_MT_prism(Menu):
        bl_label = "Prism (Safe Mode)"
        
        def draw(self, context):
            layout = self.layout
            layout.operator("prism.safe_project_browser")
            layout.operator("prism.safe_settings")
            layout.separator()
            layout.operator("prism.about")
    
    # Register classes
    def register():
        bpy.utils.register_class(PRISM_OT_safe_project_browser)
        bpy.utils.register_class(PRISM_OT_safe_settings)
        bpy.utils.register_class(PRISM_OT_about)
        bpy.utils.register_class(TOPBAR_MT_prism)
        
        # Add to top bar
        bpy.types.TOPBAR_MT_editor_menus.append(menu_draw)
    
    def unregister():
        bpy.utils.unregister_class(PRISM_OT_safe_project_browser)
        bpy.utils.unregister_class(PRISM_OT_safe_settings)
        bpy.utils.unregister_class(PRISM_OT_about)
        bpy.utils.unregister_class(TOPBAR_MT_prism)
        
        bpy.types.TOPBAR_MT_editor_menus.remove(menu_draw)
    
    def menu_draw(self, context):
        self.layout.menu("TOPBAR_MT_prism")
    
    # Auto-register when script loads
    register()
    print("Prism: Safe mode registered successfully")
    
except Exception as e:
    print(f"Prism: Failed to initialize safely - {{e}}")
    import traceback
    traceback.print_exc()
'''

print("Creating Safe Prism Integration")
print("=" * 50)

# Create in user's Blender config (safer than system-wide)
blender_user_startup = os.path.expanduser("~/.config/blender/4.5/scripts/startup")
os.makedirs(blender_user_startup, exist_ok=True)

safe_init_path = os.path.join(blender_user_startup, "PrismInitSafe.py")

try:
    with open(safe_init_path, 'w') as f:
        f.write(safe_content)
    print(f"✓ Created safe Prism init at: {safe_init_path}")
    print("\nNow:")
    print("1. Remove or rename the system PrismInit.py:")
    print("   sudo mv /usr/share/blender/4.5/scripts/startup/PrismInit.py /usr/share/blender/4.5/scripts/startup/PrismInit.py.disabled")
    print("2. Launch Blender normally:")
    print("   blender")
    print("3. You should see 'Prism (Safe Mode)' in the menu")
    
except Exception as e:
    print(f"❌ Failed to create safe init: {e}")