"""
Advanced Qt test in Blender - test various Qt features that Prism uses
"""
import sys
import os
import traceback

try:
    from PySide2.QtWidgets import *
    from PySide2.QtCore import *
    print("Using PySide2")
except:
    try:
        from PyQt5.QtWidgets import *
        from PyQt5.QtCore import *
        print("Using PyQt5")
    except:
        print("No Qt found!")
        sys.exit(1)

class TestDialog(QDialog):
    """Test various Qt features"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Qt Feature Test")
        self.setMinimumSize(400, 500)
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout()
        
        # Test 1: Labels and basic widgets
        layout.addWidget(QLabel("=== Qt Feature Tests ==="))
        
        # Test 2: Line Edit (text input)
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter project name...")
        layout.addWidget(QLabel("Test LineEdit:"))
        layout.addWidget(self.name_input)
        
        # Test 3: ComboBox (dropdown)
        self.combo = QComboBox()
        self.combo.addItems(["Option 1", "Option 2", "Option 3"])
        layout.addWidget(QLabel("Test ComboBox:"))
        layout.addWidget(self.combo)
        
        # Test 4: Tree Widget (like Prism uses for projects)
        self.tree = QTreeWidget()
        self.tree.setHeaderLabels(["Name", "Type"])
        root = QTreeWidgetItem(self.tree, ["Projects", "Folder"])
        child1 = QTreeWidgetItem(root, ["TestProject", "Project"])
        child2 = QTreeWidgetItem(root, ["Assets", "Folder"])
        layout.addWidget(QLabel("Test TreeWidget:"))
        layout.addWidget(self.tree)
        
        # Test 5: Tab Widget
        self.tabs = QTabWidget()
        self.tabs.addTab(QWidget(), "General")
        self.tabs.addTab(QWidget(), "Settings")
        layout.addWidget(QLabel("Test TabWidget:"))
        layout.addWidget(self.tabs)
        
        # Test 6: File Dialog button
        file_btn = QPushButton("Test File Dialog")
        file_btn.clicked.connect(self.test_file_dialog)
        layout.addWidget(file_btn)
        
        # Test 7: Message Box button
        msg_btn = QPushButton("Test Message Box")
        msg_btn.clicked.connect(self.test_message_box)
        layout.addWidget(msg_btn)
        
        # Test 8: Progress Dialog button
        progress_btn = QPushButton("Test Progress Dialog")
        progress_btn.clicked.connect(self.test_progress_dialog)
        layout.addWidget(progress_btn)
        
        # Test 9: Nested Dialog button
        nested_btn = QPushButton("Test Nested Dialog")
        nested_btn.clicked.connect(self.test_nested_dialog)
        layout.addWidget(nested_btn)
        
        # Results display
        self.results = QTextEdit()
        self.results.setMaximumHeight(100)
        self.results.setReadOnly(True)
        layout.addWidget(QLabel("Results:"))
        layout.addWidget(self.results)
        
        # Close button
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn)
        
        self.setLayout(layout)
        self.log("Dialog created successfully")
    
    def log(self, message):
        """Add message to results"""
        self.results.append(message)
        print(message)
    
    def test_file_dialog(self):
        """Test file dialog (common crash point)"""
        try:
            path = QFileDialog.getExistingDirectory(self, "Select Directory")
            if path:
                self.log(f"✓ File dialog worked: {path}")
            else:
                self.log("✓ File dialog cancelled (working)")
        except Exception as e:
            self.log(f"✗ File dialog failed: {e}")
            traceback.print_exc()
    
    def test_message_box(self):
        """Test message box"""
        try:
            reply = QMessageBox.question(self, "Test", "Does this message box work?",
                                        QMessageBox.Yes | QMessageBox.No)
            self.log(f"✓ Message box worked: {reply}")
        except Exception as e:
            self.log(f"✗ Message box failed: {e}")
    
    def test_progress_dialog(self):
        """Test progress dialog"""
        try:
            progress = QProgressDialog("Testing...", "Cancel", 0, 100, self)
            progress.setWindowModality(Qt.WindowModal)
            
            for i in range(101):
                progress.setValue(i)
                if progress.wasCanceled():
                    break
                QApplication.processEvents()
            
            self.log("✓ Progress dialog worked")
        except Exception as e:
            self.log(f"✗ Progress dialog failed: {e}")
    
    def test_nested_dialog(self):
        """Test opening another dialog (like Prism does)"""
        try:
            nested = QDialog(self)
            nested.setWindowTitle("Nested Dialog")
            layout = QVBoxLayout()
            layout.addWidget(QLabel("This is a nested dialog"))
            btn = QPushButton("Close")
            btn.clicked.connect(nested.accept)
            layout.addWidget(btn)
            nested.setLayout(layout)
            nested.exec_()
            self.log("✓ Nested dialog worked")
        except Exception as e:
            self.log(f"✗ Nested dialog failed: {e}")
            traceback.print_exc()

def test_with_prism_paths():
    """Test with Prism paths set (like the real environment)"""
    # Set Prism environment
    prism_path = "/home/lmarch/src/Prism/Prism"
    os.environ["PRISM_ROOT"] = prism_path
    os.environ["PRISM_LIBS"] = prism_path
    os.environ["PRISM_NO_LIBS"] = "1"
    
    # Add Prism to path
    prism_scripts = os.path.join(prism_path, "Scripts")
    if prism_scripts not in sys.path:
        sys.path.insert(0, prism_scripts)
    
    print("Environment set like Prism")
    return True

# Main test
def run_tests():
    print("=" * 50)
    print("Starting Qt tests in Blender")
    print("=" * 50)
    
    # Check for existing QApplication
    app = QApplication.instance()
    if not app:
        app = QApplication(sys.argv)
        print("Created new QApplication")
    else:
        print("Using existing QApplication")
    
    # Optional: Set up Prism-like environment
    # Uncomment to test with Prism paths:
    # test_with_prism_paths()
    
    # Create and show dialog
    dialog = TestDialog()
    result = dialog.exec_()
    
    print("=" * 50)
    if result:
        print("✓ All Qt tests completed!")
    else:
        print("Tests cancelled")
    print("=" * 50)

# Run the tests
run_tests()