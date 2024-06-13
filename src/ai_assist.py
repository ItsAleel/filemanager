import os
import re
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtCore import QDir
from dotenv import load_dotenv
from groq import Groq

class AIAssist:
    def __init__(self, status_bar):
        self.status_bar = status_bar
        load_dotenv(os.path.join(os.path.dirname(__file__), 'settings', 'secret', '.env'))
        self.api_key = os.getenv('GROQ_API_KEY')
        self.client = Groq(api_key=self.api_key)
        self.base_path = QDir.currentPath()

    def set_base_path(self, path):
        self.base_path = path

    def ai_import_code_into_file(self, code):
        try:
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": f"Where should the following code be imported to? {code}"
                    }
                ],
                model="mixtral-8x7b-32768",
            )
            file_path = chat_completion.choices[0].message.content.strip()

            if file_path:
                full_path = os.path.join(self.base_path, file_path)
                os.makedirs(os.path.dirname(full_path), exist_ok=True)
                with open(full_path, 'w', encoding='utf-8') as file:
                    file.write(code)
                self.status_bar.showMessage(f"Code imported into: {full_path}")
                return full_path
            else:
                QMessageBox.critical(None, "AI Assist Error", "AI assist failed to determine file path.")
                return None
        except Exception as e:
            QMessageBox.critical(None, "Error", f"An error occurred while using AI assist: {e}")
            return None

    def ai_create_file_structure(self, structure):
        try:
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": f"Please convert the following description into a detailed file directory structure. Each directory and file should be on a new line:\n\n{structure}"
                    }
                ],
                model="mixtral-8x7b-32768",
            )
            formatted_structure = chat_completion.choices[0].message.content.strip()

            print(f"AI Response: {formatted_structure}")  # Debugging

            if formatted_structure.startswith("Here is the detailed file structure"):
                formatted_structure = formatted_structure.replace("Here is the detailed file structure:", "").strip()

            invalid_chars = r'[<>:"/\\|?*]'

            for line in formatted_structure.split('\n'):
                line = line.strip()
                if not line:
                    continue
                if re.search(invalid_chars, line):
                    print(f"Skipping invalid path: {line}")  # Debugging
                    continue
                print(f"Processing line: {line}")  # Debugging
                if line.endswith('/'):
                    directory_path = os.path.join(self.base_path, line.rstrip('/'))
                    print(f"Creating directory: {directory_path}")  # Debugging
                    os.makedirs(directory_path, exist_ok=True)
                else:
                    file_path = os.path.join(self.base_path, line)
                    print(f"Creating file: {file_path}")  # Debugging
                    os.makedirs(os.path.dirname(file_path), exist_ok=True)
                    open(file_path, 'a').close()

            self.status_bar.showMessage("File structure created successfully.")
        except Exception as e:
            QMessageBox.critical(None, "Error", f"An error occurred while using AI assist: {e}")
            self.status_bar.showMessage(f"Error creating file structure: {e}")
