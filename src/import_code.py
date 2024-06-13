import os
from PyQt6.QtWidgets import QMessageBox

class CodeImport:
    def __init__(self, status_bar):
        self.status_bar = status_bar

    def import_code_into_file(self, file_path, code):
        try:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(code)
            self.status_bar.showMessage(f"Code imported into: {file_path}")
        except Exception as e:
            QMessageBox.critical(None, "Error", f"Could not import code into {file_path}. Error: {e}")
