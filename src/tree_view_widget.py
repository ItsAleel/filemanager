# ai_assist.py

import os
from PyQt6.QtCore import QDir, Qt, pyqtSignal
import re
import threading
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtCore import QDir, QObject, QThread, pyqtSignal
from dotenv import load_dotenv
from groq import Groq

class AIWorker(QObject):
    finished = pyqtSignal()
    error = pyqtSignal(Exception)
    result = pyqtSignal(str)
    log = pyqtSignal(str)

    def __init__(self, api_key, current_directory, code, prompt_template):
        super().__init__()
        self.api_key = api_key
        self.current_directory = current_directory
        self.code = code
        self.prompt_template = prompt_template

    def run(self):
        try:
            client = Groq(api_key=self.api_key)
            prompt = self.prompt_template.format(
                current_directory=self.current_directory,
                code=self.code
            )
            self.log.emit(f"Prompt to AI:\n{prompt}")
            chat_completion = client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a helpful assistant. When provided with code, "
                            "you must respond with the relative file path where the code should be placed. "
                            "Respond only with the relative file path and nothing else."
                        )
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                model="mixtral-8x7b-32768",
                temperature=0.3,
                top_p=1
            )
            response = chat_completion.choices[0].message.content.strip()
            self.log.emit(f"Response from AI:\n{response}")

            relative_file_path = self._sanitize_path(response)
            full_path = os.path.normpath(os.path.join(self.current_directory, relative_file_path))
            self.log.emit(f"Full path to write code: {full_path}")

            if not self._is_path_within_directory(full_path, self.current_directory):
                raise ValueError(f"Invalid file path received from AI assist: '{relative_file_path}' is outside the current directory.")
            
            if not os.path.exists(full_path):
                raise FileNotFoundError(f"File does not exist: {full_path}")
            
            self._append_code_to_file(full_path, self.code)

            self.result.emit(full_path)
        except Exception as e:
            self.error.emit(e)
        finally:
            self.finished.emit()

    def _sanitize_path(self, path):
        if os.path.isabs(path):
            path = os.path.relpath(path, self.current_directory)
        path = os.path.normpath(path)
        if not re.match(r'^[\w\-. /\\]+$', path):
            raise ValueError(f"Invalid file path received from AI assist: '{path}'")
        return path

    def _is_path_within_directory(self, path, directory):
        # Ensure the given path is within the specified directory
        abs_path = os.path.abspath(path)
        abs_directory = os.path.abspath(directory)
        return abs_path.startswith(abs_directory)

    def _append_code_to_file(self, path, code):
        try:
            lock = threading.Lock()
            with lock:
                with open(path, 'a+', encoding='utf-8') as file:
                    file.seek(0)
                    original_content = file.read()
                    self.log.emit(f"Original content of the file: {original_content}")
                    file.write(f"\n{code}\n")
                    self.log.emit(f"Appended code to file: {code}")
                with open(path, 'r', encoding='utf-8') as file:
                    contents = file.read()
                    self.log.emit(f"Final content of the file: {contents}")
                    if f"\n{code}\n" not in contents[len(original_content):]:
                        raise IOError("Code was not appended correctly.")
        except Exception as e:
            self.log.emit(f"Error appending code to file: {e}")
            raise

class AIAssist:
    def __init__(self, status_bar, console_logger):
        self.status_bar = status_bar
        self.console_logger = console_logger
        load_dotenv(os.path.join(os.path.dirname(__file__), 'settings', 'secret', '.env'))
        self.api_key = os.getenv('GROQ_API_KEY')
        self.current_directory = QDir.currentPath()
        self.thread = None

    def set_current_directory(self, path):
        self.current_directory = os.path.abspath(path)

    def log(self, message):
        self.console_logger.log_message(message)

    def ai_import_code_into_file(self, code, current_directory):
        prompt_template = (
            "The current directory is: {current_directory}\n"
            "Please provide the relative file path (relative to the current directory) where the following code should be placed.\n"
            "Code:\n{code}\n"
            "Respond with the relative file path only. Do not include any other text."
        )
        self._run_ai_task(code, current_directory, prompt_template)

    def ai_create_file_structure(self, structure, current_directory):
        prompt_template = (
            "The current directory is: {current_directory}\n"
            "Convert the following description into a valid file directory structure within the current directory, "
            "with each directory and file on a new line, properly formatted with full paths:\n\n{structure}"
        )
        self._run_ai_task(structure, current_directory, prompt_template)

    def _run_ai_task(self, content, current_directory, prompt_template):
        self.worker = AIWorker(self.api_key, current_directory, content, prompt_template)
        self.thread = QThread()
        self.worker.moveToThread(self.thread)

        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)

        self.worker.log.connect(self.log)
        self.worker.result.connect(self.handle_result)
        self.worker.error.connect(self.handle_error)

        self.thread.started.connect(self.worker.run)
        self.thread.start()

    def handle_result(self, full_path):
        self.status_bar.showMessage(f"Code imported into: {full_path}")
        self.log(f"Code successfully imported into: {full_path}")

    def handle_error(self, error):
        self.status_bar.showMessage(f"Error importing code: {error}")
        self.log(f"Error importing code: {error}")
        QMessageBox.critical(None, "Error", f"An error occurred while using AI assist: {error}")
