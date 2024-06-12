import os
import logging
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QTabWidget, QTextEdit, QLineEdit, QPushButton,
    QLabel, QScrollArea, QMessageBox, QFileDialog, QToolBar, QStatusBar, QMainWindow
)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import QDir

# Setup logging
logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

class MainContentWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)

        self.tab_widget = QTabWidget(self)
        self.status_bar = QStatusBar(self)

        self.setup_text_editor()
        self.setup_image_viewer()
        self.setup_tabs()
        self.setup_toolbar()

        self.layout.addWidget(self.tab_widget)
        self.layout.addWidget(self.status_bar)
        self.setLayout(self.layout)

    def setup_toolbar(self):
        self.toolbar = QToolBar(self)
        self.layout.insertWidget(0, self.toolbar)

        self.save_button = QPushButton("Save", self)
        self.save_button.clicked.connect(self.save_code)
        self.toolbar.addWidget(self.save_button)

        self.select_file_button = QPushButton("Select File", self)
        self.select_file_button.clicked.connect(self.select_file)
        self.toolbar.addWidget(self.select_file_button)

    def setup_text_editor(self):
        self.text_editor = QTextEdit(self)

    def setup_image_viewer(self):
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.image_viewer = QLabel(self.scroll_area)
        self.image_viewer.setScaledContents(True)
        self.scroll_area.setWidget(self.image_viewer)

    def setup_tabs(self):
        self.setup_code_input_tab()
        self.setup_file_structure_tab()

        self.tab_widget.addTab(self.text_editor, "Text Editor")
        self.tab_widget.addTab(self.scroll_area, "Image Viewer")
        self.tab_widget.addTab(self.code_input_tab, "Code Input")
        self.tab_widget.addTab(self.file_structure_tab, "File Structure")

    def setup_file_structure_tab(self):
        self.file_structure_tab = QWidget()
        self.file_structure_layout = QVBoxLayout(self.file_structure_tab)
        
        self.file_structure_input = QLineEdit(self.file_structure_tab)
        self.file_structure_input.setPlaceholderText("Enter file structure here (e.g., folder1, folder2/file.txt)...")

        self.file_structure_button = QPushButton("Create File Structure")
        self.file_structure_button.clicked.connect(self.create_file_structure)

        self.file_structure_layout.addWidget(self.file_structure_input)
        self.file_structure_layout.addWidget(self.file_structure_button)
        self.file_structure_tab.setLayout(self.file_structure_layout)

    def setup_code_input_tab(self):
        self.code_input_tab = QWidget()
        self.code_input_layout = QVBoxLayout(self.code_input_tab)

        self.code_input_box = QLineEdit(self.code_input_tab)
        self.code_input_box.setPlaceholderText("Enter code here...")

        self.save_code_button = QPushButton("Save Code")
        self.save_code_button.clicked.connect(self.save_code)

        self.select_file_button = QPushButton("Select File")
        self.select_file_button.clicked.connect(self.select_file)

        self.selected_file_label = QLabel("No file selected")

        self.code_input_layout.addWidget(self.selected_file_label)
        self.code_input_layout.addWidget(self.code_input_box)
        self.code_input_layout.addWidget(self.save_code_button)
        self.code_input_layout.addWidget(self.select_file_button)
        self.code_input_tab.setLayout(self.code_input_layout)

    def display_content(self, path):
        if path.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            self.display_image(path)
        else:
            self.display_text(path)

    def display_text(self, path):
        try:
            with open(path, 'r', encoding='utf-8') as file:
                content = file.read()
                self.text_editor.setText(content)
                self.code_input_box.setText(content)
                self.tab_widget.setCurrentWidget(self.text_editor)
                self.status_bar.showMessage(f"Opened {path}")
        except Exception as e:
            logging.error(f"Could not read file {path}. Error: {e}")
            QMessageBox.critical(self, "Error", f"Could not read file {path}. Error: {e}")

    def display_image(self, path):
        try:
            pixmap = QPixmap(path)
            self.image_viewer.setPixmap(pixmap)
            self.tab_widget.setCurrentWidget(self.scroll_area)
            self.status_bar.showMessage(f"Opened {path}")
        except Exception as e:
            logging.error(f"Could not display image {path}. Error: {e}")
            QMessageBox.critical(self, "Error", f"Could not display image {path}. Error: {e}")

    def save_code(self):
        path = self.selected_file_label.text().strip()
        if os.path.exists(path):
            try:
                with open(path, 'w', encoding='utf-8') as file:
                    file.write(self.text_editor.toPlainText())
                QMessageBox.information(self, "Success", f"Code saved to: {path}")
                self.status_bar.showMessage(f"Code saved to {path}")
            except Exception as e:
                logging.error(f"Could not save code to {path}. Error: {e}")
                QMessageBox.critical(self, "Error", f"Could not save code to {path}. Error: {e}")
        else:
            QMessageBox.warning(self, "Error", "Invalid file path.")

    def select_file(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(self, "Select File to Save Code", "", "All Files (*);;Text Files (*.txt)", options=options)
        if file_path:
            self.selected_file_label.setText(file_path)
            self.status_bar.showMessage(f"Selected file: {file_path}")

    def create_file_structure(self):
        structure = self.file_structure_input.text()
        base_path = QDir.rootPath()  # Default to root path if no model is available
        try:
            for part in structure.split(','):
                part = part.strip()
                if part:
                    path = os.path.join(base_path, part)
                    if '.' in part:
                        open(path, 'a').close()
                    else:
                        os.makedirs(path, exist_ok=True)
            QMessageBox.information(self, "Success", "File structure created successfully.")
            self.status_bar.showMessage("File structure created successfully.")
        except Exception as e:
            logging.error(f"Could not create file structure. Error: {e}")
            QMessageBox.critical(self, "Error", f"Could not create file structure. Error: {e}")
