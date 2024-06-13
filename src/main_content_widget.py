import os
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QTabWidget, QTextEdit, QPushButton, QLabel, QScrollArea,
                             QMessageBox, QFileDialog, QStatusBar, QHBoxLayout, QCheckBox)
from PyQt6.QtGui import QPixmap, QIcon
from PyQt6.QtCore import QDir, QTimer, Qt
from file_structure import FileStructure
from ai_assist import AIAssist

class MainContentWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.layout = QVBoxLayout(self)

        self.status_bar = QStatusBar(self)
        self.status_bar.showMessage("Ready")

        self.tab_widget = QTabWidget(self)
        self.text_editor = QTextEdit(self)
        self.setup_image_viewer()

        self.tab_widget.addTab(self.text_editor, "Text/Code Editor")
        self.tab_widget.addTab(self.scroll_area, "Image Viewer")

        self.layout.addWidget(self.tab_widget)
        self.layout.addWidget(self.status_bar)
        self.setLayout(self.layout)

        self.setup_bottom_right_buttons()

        self.current_file_path = None
        self.selected_file_path = None
        self.setup_auto_save()

        self.is_ai_assist = False
        self.file_structure = FileStructure(self.status_bar)
        self.ai_assist = AIAssist(self.status_bar)

    def setup_image_viewer(self):
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.image_viewer = QLabel(self.scroll_area)
        self.image_viewer.setScaledContents(True)
        self.scroll_area.setWidget(self.image_viewer)

    def setup_auto_save(self):
        self.auto_save_timer = QTimer(self)
        self.auto_save_timer.timeout.connect(self.auto_save)
        self.auto_save_timer.start(300000)  # Auto-save every 5 minutes

    def setup_bottom_right_buttons(self):
        self.bottom_right_layout = QHBoxLayout()

        self.save_button = QPushButton(QIcon.fromTheme("document-save"), "Save", self)
        self.save_button.clicked.connect(self.save_code)
        self.bottom_right_layout.addWidget(self.save_button)

        self.create_structure_button = QPushButton("Create File Structure")
        self.create_structure_button.clicked.connect(self.create_file_structure)
        self.bottom_right_layout.addWidget(self.create_structure_button)

        self.import_code_button = QPushButton("Import Code into File")
        self.import_code_button.clicked.connect(self.import_code_into_file)
        self.bottom_right_layout.addWidget(self.import_code_button)

        self.ai_assist_toggle = QCheckBox("AI Assist", self)
        self.ai_assist_toggle.toggled.connect(self.toggle_ai_assist)
        self.bottom_right_layout.addWidget(self.ai_assist_toggle)

        self.bottom_right_layout.addStretch()
        self.layout.addLayout(self.bottom_right_layout)

    def toggle_ai_assist(self, checked):
        self.is_ai_assist = checked
        print(f"AI Assist toggled {'on' if self.is_ai_assist else 'off'}")

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
                self.current_file_path = path
                self.tab_widget.setCurrentWidget(self.text_editor)
                self.status_bar.showMessage(f"Opened {path}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not read file {path}. Error: {e}")

    def display_image(self, path):
        try:
            pixmap = QPixmap(path)
            self.image_viewer.setPixmap(pixmap)
            self.tab_widget.setCurrentWidget(self.scroll_area)
            self.status_bar.showMessage(f"Opened {path}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not display image {path}. Error: {e}")

    def save_code(self):
        if not self.current_file_path:
            self.select_file()
        if self.current_file_path:
            try:
                with open(self.current_file_path, 'w', encoding='utf-8') as file:
                    file.write(self.text_editor.toPlainText())
                self.status_bar.showMessage(f"Code saved to: {self.current_file_path}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Could not save code to {self.current_file_path}. Error: {e}")

    def auto_save(self):
        if self.current_file_path:
            self.save_code()

    def import_code_into_file(self):
        if self.is_ai_assist:
            self.ai_import_code_into_file()
        else:
            if self.selected_file_path:
                try:
                    with open(self.selected_file_path, 'w', encoding='utf-8') as file:
                        file.write(self.text_editor.toPlainText())
                    self.status_bar.showMessage(f"Code imported into: {self.selected_file_path}")
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"Could not import code into {self.selected_file_path}. Error: {e}")
            else:
                QMessageBox.warning(self, "No File Selected", "Please select a file from the directory tree to import code.")

    def ai_import_code_into_file(self):
        code = self.text_editor.toPlainText()
        file_path = self.ai_assist.ai_import_code_into_file(code)
        if file_path:
            self.selected_file_path = file_path

    def set_base_path(self, path):
        self.file_structure.set_base_path(path)
        self.ai_assist.set_base_path(path)  # Ensure AI Assist uses the same base path

    def set_selected_file_path(self, path):
        self.selected_file_path = path

    def select_file(self):
        options = QFileDialog.Option.DontUseNativeDialog
        file_path, _ = QFileDialog.getSaveFileName(self, "Select File to Save Code", "", "All Files (*);;Text Files (*.txt)", options=options)
        if file_path:
            self.current_file_path = file_path
            self.status_bar.showMessage(f"Selected file: {file_path}")

    def create_file_structure(self):
        structure = self.text_editor.toPlainText()
        if self.is_ai_assist:
            print("Using AI Assist to create file structure")  # Debugging
            self.ai_assist.ai_create_file_structure(structure)
        else:
            print("Using manual method to create file structure")  # Debugging
            self.file_structure.create_file_structure(structure)
