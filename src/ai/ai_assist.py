# src/ai/ai_assist.py
import os
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

    def __init__(self, api_key, current_directory, content, prompt_template):
        super().__init__()
        self.api_key = api_key
        self.current_directory = current_directory
        self.content = content
        self.prompt_template = prompt_template

    def run(self):
        try:
            client = Groq(api_key=self.api_key)
            prompt = self.prompt_template.format(
                current_directory=self.current_directory,
                content=self.content
            )
            self.log.emit(f"Prompt to AI:\n{prompt}")
            chat_completion = client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a helpful assistant. When provided with a description of a file structure, "
                            "you must respond with the properly formatted structure to create the directories and files. "
                            "Respond only with the formatted structure and nothing else."
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

            # Use the formatted structure directly to create directories and files
            self._create_structure_from_response(response)

            self.result.emit(self.current_directory)
        except Exception as e:
            self.error.emit(e)
        finally:
            self.finished.emit()

    def _sanitize_path(self, path):
        if os.path.isabs(path):
            path = os.path.relpath(path, self.current_directory)
        path = os.path.normpath(path).replace("\\_", "_")  # Replace incorrect backslashes
        if not re.match(r'^[\w\-. /\\]+$', path):
            raise ValueError(f"Invalid path received from AI assist: '{path}'")
        return path

    def _extract_paths(self, response):
        # Split the response by new lines to get individual paths
        paths = response.split('\n')
        sanitized_paths = [self._sanitize_path(path.strip()) for path in paths if path.strip()]
        return sanitized_paths

    def _is_path_within_directory(self, path, directory):
        # Ensure the given path is within the specified directory
        abs_path = os.path.abspath(path)
        abs_directory = os.path.abspath(directory)
        return abs_path.startswith(abs_directory)

    def _create_directory(self, path):
        """Create a directory at the given path.

        Args:
            path (str): The path of the directory to create.
        """
        os.makedirs(path, exist_ok=True)
        self.log.emit(f"Created directory: {path}")

    def _create_file(self, path):
        """Create a file at the given path.

        Args:
            path (str): The path of the file to create.
        """
        os.makedirs(os.path.dirname(path), exist_ok=True)
        open(path, 'a').close()
        self.log.emit(f"Created file: {path}")

    def _create_structure_from_response(self, response):
        """Create the file structure from the AI response.

        Args:
            response (str): The formatted structure from the AI response.
        """
        lines = response.split('\n')
        stack = [self.current_directory]

        for line in lines:
            line = line.rstrip()
            if not line:
                continue

            depth = self._get_indent_level(line)

            clean_line = line.lstrip(' ┣┃┗').strip()
            if not clean_line:
                continue

            path_parts = self._extract_path_parts(clean_line)

            while depth < len(stack) - 1:
                stack.pop()

            current_path = os.path.join(stack[-1], *path_parts)

            if '.' in os.path.basename(current_path):  # It's a file
                self._create_file(current_path)
            else:  # It's a directory
                self._create_directory(current_path)
                if depth >= len(stack):
                    stack.append(current_path)

    def _get_indent_level(self, line: str) -> int:
        """Get the indent level of a line in the input structure.

        Args:
            line (str): The line from the input structure.

        Returns:
            int: The indent level of the line.
        """
        return len(line) - len(line.lstrip(' ┣┃┗'))

    def _extract_path_parts(self, line: str) -> list:
        """Extract the path parts from a line in the input structure.

        Args:
            line (str): The line from the input structure.

        Returns:
            list: A list of path parts.
        """
        parts = []
        special_chars = ['📦', '📂', '📜', '┣', '┃', '┗']
        for part in line.split():
            part = part.strip()
            for char in special_chars:
                part = part.replace(char, '')
            if part:
                parts.append(part)
        return parts

class AIAssist:
    def __init__(self, status_bar, console_logger):
        self.status_bar = status_bar
        self.console_logger = console_logger
        load_dotenv(os.path.join(os.path.dirname(__file__), '../settings/secret/.env'))
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
            "Code:\n{content}\n"
            "Respond with the relative file path only. Do not include any other text."
        )
        self._run_ai_task(code, current_directory, prompt_template)

    def ai_create_file_structure(self, structure, current_directory):
        prompt_template = (
            "The current directory is: {current_directory}\n"
            "Convert the following description into a properly formatted file directory structure within the current directory:\n\n{content}"
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
        self.status_bar.showMessage(f"Content imported into: {full_path}")
        self.log(f"Content successfully imported into: {full_path}")

    def handle_error(self, error):
        self.status_bar.showMessage(f"Error importing content: {error}")
        self.log(f"Error importing content: {error}")
        QMessageBox.critical(None, "Error", f"An error occurred while using AI assist: {error}")
