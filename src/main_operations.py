# main_operations.py

import os
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QSplitter, QPushButton, QLineEdit, QComboBox, QHBoxLayout, QMessageBox
from tree_view_widget import TreeViewWidget
from main_content_widget import MainContentWidget

class MainOperations(QWidget):
    def __init__(self, parent=None, console_tab=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.splitter = QSplitter(Qt.Orientation.Horizontal, self)

        # Navigation layout
        self.nav_layout = QHBoxLayout()
        
        # Back button
        self.back_button = QPushButton("<")
        self.nav_layout.addWidget(self.back_button)
        
        # Drive selector
        self.drive_selector = QComboBox()
        self.nav_layout.addWidget(self.drive_selector)

        # Directory input
        self.dir_input = QLineEdit(self)
        self.dir_input.setPlaceholderText("Enter directory...")
        self.nav_layout.addWidget(self.dir_input)

        # Search bar
        self.search_bar = QLineEdit(self)
        self.search_bar.setPlaceholderText("Search...")
        self.nav_layout.addWidget(self.search_bar)
        
        # Add navigation layout to the main layout
        self.layout.addLayout(self.nav_layout)

        # Initialize Tree View and Main Content
        self.tree_view = TreeViewWidget(self)
        self.main_content = MainContentWidget(self, console_tab)  # Pass console_tab to MainContentWidget

        # Add widgets to splitter
        self.splitter.addWidget(self.tree_view)
        self.splitter.addWidget(self.main_content)

        # Add splitter to main layout
        self.layout.addWidget(self.splitter)
        self.setLayout(self.layout)

        self.splitter.setSizes([300, 700])

        # Connect signals
        self.tree_view.file_double_clicked.connect(self.main_content.display_content)
        self.tree_view.dir_changed.connect(self.update_directory_input)
        self.tree_view.dir_changed.connect(self.clear_search_bar)
        self.tree_view.dir_changed.connect(self.on_directory_changed)  # Updated to use on_directory_changed
        self.tree_view.file_selected.connect(self.main_content.set_selected_file_path)
        self.search_bar.textChanged.connect(self.on_search_text_changed)
        self.back_button.clicked.connect(self.go_back)
        self.drive_selector.currentIndexChanged.connect(self.on_drive_selected)
        self.dir_input.returnPressed.connect(self.on_enter_directory)

        # Populate drives
        self.populate_drives()

    def populate_drives(self):
        drives = [f"{d}:\\" for d in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' if os.path.exists(f"{d}:\\")]
        self.drive_selector.addItems(drives)
        self.drive_selector.setCurrentIndex(0)
        self.dir_input.setText(drives[0])

    def go_back(self):
        current_path = self.tree_view.model.rootPath()
        parent_path = os.path.abspath(os.path.join(current_path, os.pardir))
        self.tree_view.set_root_directory(parent_path)
        self.dir_input.setText(parent_path)

    def on_drive_selected(self, index):
        drive = self.drive_selector.itemText(index)
        self.tree_view.set_root_directory(drive)
        self.dir_input.setText(drive)

    def on_enter_directory(self):
        path = self.dir_input.text()
        if os.path.exists(path):
            self.tree_view.set_root_directory(path)
        else:
            QMessageBox.warning(self, "Invalid Path", f"Path '{path}' does not exist.")

    def on_search_text_changed(self, text):
        self.tree_view.model.setNameFilters([f"*{text}*"])
        self.tree_view.model.setNameFilterDisables(False)

    def update_directory_input(self, path):
        self.dir_input.setText(path)

    def clear_search_bar(self, path):
        self.search_bar.clear()

    def on_directory_changed(self, path):
        self.main_content.current_directory = path  # Directly update current_directory attribute
        self.main_content.ai_assist.set_current_directory(path)  # Update the current directory in AI Assist
