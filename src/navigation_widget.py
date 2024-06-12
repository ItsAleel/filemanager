import os
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QComboBox, QPushButton, QMessageBox
from PyQt6.QtCore import QDir, pyqtSignal

class NavigationWidget(QWidget):
    dir_changed = pyqtSignal(str)
    search_text_changed = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        
        # Back button
        self.back_button = QPushButton("<")
        self.back_button.clicked.connect(self.go_back)
        self.previous_directories = []

        # Directory Navigation
        self.dir_input = QLineEdit(self)
        self.dir_input.setPlaceholderText("Enter directory...")
        self.dir_input.returnPressed.connect(self.on_enter_directory)

        self.drive_selector = QComboBox(self)
        self.populate_drives()
        self.drive_selector.currentIndexChanged.connect(self.on_drive_selected)

        self.search_bar = QLineEdit(self)
        self.search_bar.setPlaceholderText("Search...")
        self.search_bar.textChanged.connect(self.on_search_text_changed)

        self.nav_layout = QHBoxLayout()
        self.nav_layout.addWidget(self.back_button)
        self.nav_layout.addWidget(self.drive_selector)
        self.nav_layout.addWidget(self.dir_input)
        self.nav_layout.addWidget(self.search_bar)

        self.layout.addLayout(self.nav_layout)
        self.setLayout(self.layout)

    def populate_drives(self):
        drives = [f"{d}:\\" for d in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' if os.path.exists(f"{d}:\\")]
        self.drive_selector.addItems(drives)
        self.drive_selector.setCurrentIndex(0)
        self.dir_input.setText(drives[0])

    def on_drive_selected(self, index):
        drive = self.drive_selector.itemText(index)
        self.dir_input.setText(drive)
        self.on_enter_directory()

    def on_enter_directory(self):
        path = self.dir_input.text()
        if os.path.exists(path):
            current_path = self.dir_input.text()
            if current_path != path:
                self.previous_directories.append(current_path)
            self.dir_changed.emit(path)
        else:
            QMessageBox.warning(self, "Invalid Path", f"Path '{path}' does not exist.")

    def go_back(self):
        if self.previous_directories:
            path = self.previous_directories.pop()
            self.dir_input.setText(path)
            self.dir_changed.emit(path)

    def on_search_text_changed(self, text):
        self.search_text_changed.emit(text)
