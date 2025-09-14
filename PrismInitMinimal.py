#!/usr/bin/env python3
"""
Minimal Prism integration for Blender that avoids all crashes
"""

bl_info = {
    "name": "Prism Pipeline (Minimal)",
    "author": "Prism",
    "version": (2, 0, 17),
    "blender": (4, 0, 0),
    "location": "Top Bar > Prism",
    "description": "Minimal Prism Pipeline Integration",
    "category": "Pipeline",
}

import os
import sys
import bpy
from bpy.types import Menu, Operator

# Set up Prism paths
PRISM_PATH = "/home/lmarch/src/Prism/Prism"  # ADJUST THIS PATH

# Global variable to hold Prism core (initialized on demand)
_prism_core = None

def get_prism_core():
    """Get or create Prism core instance (lazy initialization)"""
    global _prism_core
    
    if _prism_core is None:
        try:
            # Set environment
            os.environ["PRISM_ROOT"] = PRISM_PATH
            os.environ["PRISM_LIBS"] = PRISM_PATH
            os.environ["PRISM_NO_LIBS"] = "1"
            
            # Add to path
            prism_scripts = os.path.join(PRISM_PATH, "Scripts")
            if prism_scripts not in sys.path:
                sys.path.insert(0, prism_scripts)
            
            # Import PrismCore
            import PrismCore
            
            # Create a minimal dummy parent for messageParent
            class DummyParent:
                def setWindowFlags(self, *args, **kwargs):
                    pass
                def setWindowTitle(self, *args, **kwargs):
                    pass
                def show(self):
                    pass
                def hide(self):
                    pass
            
            # Create core with dummy parent
            _prism_core = PrismCore.PrismCore(app="Blender")
            _prism_core.messageParent = DummyParent()
            
            # Clear any project auto-loading
            if _prism_core.getConfig("globals", "current project"):
                _prism_core.setConfig("globals", "current project", "")
            
            print("Prism: Core initialized successfully")
            
        except Exception as e:
            print(f"Prism: Failed to initialize core: {e}")
            _prism_core = None
    
    return _prism_core

# Operators
class PRISM_OT_save_scene(Operator):
    """Save scene with Prism naming"""
    bl_idname = "prism.save_scene"
    bl_label = "Save Scene..."
    
    def execute(self, context):
        try:
            core = get_prism_core()
            if core:
                # Try to use Prism's save function
                core.saveScene()
                self.report({'INFO'}, "Scene saved with Prism")
            else:
                self.report({'ERROR'}, "Prism core not available")
        except Exception as e:
            self.report({'ERROR'}, f"Failed: {e}")
            # Fallback to regular Blender save
            bpy.ops.wm.save_mainfile('INVOKE_DEFAULT')
        return {'FINISHED'}

class PRISM_OT_open_folder(Operator):
    """Open project folder"""
    bl_idname = "prism.open_folder"
    bl_label = "Open Project Folder"
    
    def execute(self, context):
        try:
            core = get_prism_core()
            if core and core.prismIni:
                project_path = os.path.dirname(os.path.dirname(core.prismIni))
                if os.path.exists(project_path):
                    import subprocess
                    subprocess.Popen(['xdg-open', project_path])
                    self.report({'INFO'}, f"Opened: {project_path}")
                else:
                    self.report({'WARNING'}, "No project set")
            else:
                self.report({'WARNING'}, "Prism not initialized")
        except Exception as e:
            self.report({'ERROR'}, f"Failed: {e}")
        return {'FINISHED'}

class PRISM_OT_render_setup(Operator):
    """Setup render settings"""
    bl_idname = "prism.render_setup"
    bl_label = "Render Setup"
    
    def execute(self, context):
        try:
            # Basic render setup
            scene = context.scene
            self.report({'INFO'}, f"Output: {scene.render.filepath}")
        except Exception as e:
            self.report({'ERROR'}, f"Failed: {e}")
        return {'FINISHED'}

class PRISM_OT_info(Operator):
    """Show Prism info"""
    bl_idname = "prism.info"
    bl_label = "Info"
    
    def execute(self, context):
        core = get_prism_core()
        if core:
            msg = f"Prism {core.version} - Minimal Mode for Linux"
            if core.prismIni:
                msg += f"\nProject: {os.path.dirname(os.path.dirname(core.prismIni))}"
        else:
            msg = "Prism not initialized"
        
        self.report({'INFO'}, msg)
        return {'FINISHED'}

# Menu
class TOPBAR_MT_prism_minimal(Menu):
    bl_label = "Prism"
    
    def draw(self, context):
        layout = self.layout
        
        # Basic operations that should work
        layout.operator("prism.save_scene", icon='FILE_TICK')
        layout.operator("prism.open_folder", icon='FILE_FOLDER')
        layout.operator("prism.render_setup", icon='RENDER_STILL')
        layout.separator()
        layout.operator("prism.info", icon='INFO')

def menu_draw(self, context):
    self.layout.menu("TOPBAR_MT_prism_minimal")

# Registration
classes = [
    PRISM_OT_save_scene,
    PRISM_OT_open_folder,
    PRISM_OT_render_setup,
    PRISM_OT_info,
    TOPBAR_MT_prism_minimal,
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.TOPBAR_MT_editor_menus.append(menu_draw)
    print("Prism: Minimal integration registered")

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    bpy.types.TOPBAR_MT_editor_menus.remove(menu_draw)
    print("Prism: Minimal integration unregistered")

if __name__ == "__main__":
    register()