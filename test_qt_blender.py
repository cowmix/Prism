"""
Test Qt in Blender - run this in Blender's Text Editor
"""
import sys
import os

try:
    from PySide2.QtWidgets import QApplication, QDialog, QPushButton, QVBoxLayout, QLabel
    print("Using PySide2")
except:
    try:
        from PyQt5.QtWidgets import QApplication, QDialog, QPushButton, QVBoxLayout, QLabel
        print("Using PyQt5")
    except:
        print("No Qt found! Install with: pip install PySide2")
        sys.exit(1)

# Test 1: Simple dialog
def test_simple_dialog():
    """Test if a basic Qt dialog works"""
    app = QApplication.instance()
    if not app:
        app = QApplication(sys.argv)
    
    dialog = QDialog()
    dialog.setWindowTitle("Qt Test in Blender")
    
    layout = QVBoxLayout()
    label = QLabel("If you see this, Qt works!")
    button = QPushButton("Close")
    button.clicked.connect(dialog.accept)
    
    layout.addWidget(label)
    layout.addWidget(button)
    dialog.setLayout(layout)
    
    dialog.exec_()
    print("✓ Qt dialog worked!")

# Run the test
print("Testing Qt in Blender...")
test_simple_dialog()