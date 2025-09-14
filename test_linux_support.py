#!/usr/bin/env python3
"""
Test script to verify Linux support for Prism Blender plugin
Run this on your Linux machine to check if the changes work.
"""

import os
import sys
import platform

# Add Prism to path
prism_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(prism_root, "Prism", "Scripts"))

def test_platform_detection():
    """Test that platform is correctly detected"""
    print(f"Platform detected: {platform.system()}")
    assert platform.system() in ["Linux", "Windows", "Darwin"], "Unknown platform"
    return True

def test_qt_import():
    """Test that Qt can be imported"""
    try:
        from qtpy.QtCore import Qt
        from qtpy.QtWidgets import QApplication
        print("Qt imports successful")
        return True
    except ImportError as e:
        print(f"Qt import failed: {e}")
        return False

def test_blender_paths():
    """Test Blender path detection on Linux"""
    if platform.system() != "Linux":
        print("Skipping Linux-specific test on non-Linux platform")
        return True
    
    # Import the integration module
    sys.path.insert(0, os.path.join(prism_root, "Prism", "Plugins", "Apps", "Blender", "Scripts"))
    
    # Mock the core and plugin objects
    class MockCore:
        def __init__(self):
            self.messageParent = None
    
    class MockPlugin:
        def __init__(self):
            self.pluginName = "Blender"
    
    try:
        from Prism_Blender_Integration import Prism_Blender_Integration
        
        core = MockCore()
        plugin = MockPlugin()
        integration = Prism_Blender_Integration(core, plugin)
        
        print(f"Example path for Linux: {integration.examplePath}")
        
        # Test getExecutable
        exec_path = integration.getExecutable()
        if exec_path:
            print(f"Found Blender executable: {exec_path}")
        else:
            print("No Blender executable found (this is OK if Blender is not installed)")
        
        # Test getBlenderPaths
        paths = integration.getBlenderPaths()
        if paths:
            print(f"Found Blender paths: {paths}")
        else:
            print("No Blender paths found (this is OK if Blender is not installed)")
        
        return True
        
    except Exception as e:
        print(f"Error testing Blender integration: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all tests"""
    print("=" * 50)
    print("Testing Linux Support for Prism Blender Plugin")
    print("=" * 50)
    
    tests = [
        ("Platform Detection", test_platform_detection),
        ("Qt Import", test_qt_import),
        ("Blender Path Detection", test_blender_paths),
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\nTesting: {test_name}")
        print("-" * 30)
        success = test_func()
        results.append((test_name, success))
        print(f"Result: {'✓ PASSED' if success else '✗ FAILED'}")
    
    print("\n" + "=" * 50)
    print("Test Summary:")
    print("=" * 50)
    
    for test_name, success in results:
        status = "✓" if success else "✗"
        print(f"{status} {test_name}")
    
    all_passed = all(r[1] for r in results)
    print("\n" + ("All tests passed!" if all_passed else "Some tests failed."))
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())