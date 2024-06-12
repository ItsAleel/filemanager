import os
import sys
from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QTabWidget, QTextEdit, QPushButton, QLabel, QScrollArea,
                             QMessageBox, QFileDialog, QStatusBar, QHBoxLayout, QApplication)
from PyQt6.QtGui import QPixmap, QIcon
from PyQt6.QtCore import QDir, QTimer, Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowType.Window | Qt.WindowType.WindowTitleHint | Qt.WindowType.WindowCloseButtonHint | Qt.WindowType.WindowMinimizeButtonHint | Qt.WindowType.WindowMaximizeButtonHint)
        self.setWindowTitle("File Manager")
        self.main_widget = MainContentWidget(self)
        self.setCentralWidget(self.main_widget)

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
        self.setup_auto_save()

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
        self.import_code_button.clicked.connect(self.select_file)
        self.bottom_right_layout.addWidget(self.import_code_button)

        self.bottom_right_layout.addStretch()
        self.layout.addLayout(self.bottom_right_layout)

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

    def select_file(self):
        options = QFileDialog.Options()  # Corrected usage of QFileDialog.Options
        file_path, _ = QFileDialog.getSaveFileName(self, "Select File to Save Code", "", "All Files (*);;Text Files (*.txt)", options=options)
        if file_path:
            self.current_file_path = file_path
            self.status_bar.showMessage(f"Selected file: {file_path}")

    def create_file_structure(self):
        structure = self.text_editor.toPlainText()
        base_path = QDir.rootPath()  # Default to root path if no model is available
        try:
            for part in structure.split('\n'):
                part = part.strip()
                if part:
                    command, *args = part.split()
                    if command == "mkdir" and args:
                        os.makedirs(os.path.join(base_path, args[0]), exist_ok=True)
                    elif command == "touch" and args:
                        open(os.path.join(base_path, args[0]), 'a').close()
            self.status_bar.showMessage("File structure created successfully.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not create file structure. Error: {e}")
            self.status_bar.showMessage(f"Error creating file structure: {e}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
