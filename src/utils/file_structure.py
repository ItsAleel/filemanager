import os
from typing import List
from PyQt6.QtWidgets import QMessageBox

class FileStructureError(Exception):
    """Base class for file structure errors."""
    pass

class InvalidStructureError(FileStructureError):
    """Raised when the input structure is invalid."""
    pass

class FileStructure:
    """Class for creating a file structure based on user input."""

    def __init__(self, status_bar):
        self.status_bar = status_bar
        self.base_path = None

    def set_base_path(self, path: str):
        """Set the base path for creating the file structure.

        Args:
            path (str): The base path.
        """
        self.base_path = path

    def create_file_structure(self, structure: str):
        """Create a file structure based on the input structure.

        Args:
            structure (str): The input structure as a string.

        Raises:
            FileStructureError: If the base path is not set.
            InvalidStructureError: If the input structure is invalid.
        """
        if not self.base_path:
            raise FileStructureError("Base path is not set.")

        try:
            if self.is_valid_structure(structure):
                self._create_from_structure(structure)
            else:
                self._create_from_manual_input(structure)

            self.status_bar.showMessage("File structure created successfully.")
        except Exception as e:
            QMessageBox.critical(None, "Error", f"Could not create file structure. Error: {e}")
            self.status_bar.showMessage(f"Error creating file structure: {e}")

    def is_valid_structure(self, structure: str) -> bool:
        """Check if the input structure is valid.

        Args:
            structure (str): The input structure as a string.

        Returns:
            bool: True if the structure is valid, False otherwise.
        """
        return any(char in structure for char in ['┣', '┗', '┃', '📂', '📜'])

    def _create_from_structure(self, structure: str):
        """Create the file structure from a valid input structure.

        Args:
            structure (str): The input structure as a string.

        Raises:
            InvalidStructureError: If the input structure is invalid.
        """
        lines = structure.split('\n')
        stack = [self.base_path]

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

            if self._is_file(clean_line):
                self._create_file(current_path)
            else:
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

    def _is_file(self, line: str) -> bool:
        """Check if a line in the input structure represents a file.

        Args:
            line (str): The line from the input structure.

        Returns:
            bool: True if the line represents a file, False otherwise.
        """
        return '.' in os.path.basename(line)

    def _create_directory(self, path: str):
        """Create a directory at the given path.

        Args:
            path (str): The path of the directory to create.
        """
        os.makedirs(path, exist_ok=True)

    def _create_file(self, path: str):
        """Create a file at the given path.

        Args:
            path (str): The path of the file to create.
        """
        os.makedirs(os.path.dirname(path), exist_ok=True)
        open(path, 'a').close()

    def _extract_path_parts(self, line: str) -> List[str]:
        """Extract the path parts from a line in the input structure.

        Args:
            line (str): The line from the input structure.

        Returns:
            list[str]: A list of path parts.
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

    def _create_from_manual_input(self, structure: str):
        """Create the file structure from a manual input structure.

        Args:
            structure (str): The input structure as a string.
        """
        for line in structure.split('\n'):
            line = line.strip()
            if not line:
                continue

            if self._is_file(line):
                path = os.path.join(self.base_path, line)
                os.makedirs(os.path.dirname(path), exist_ok=True)
                open(path, 'a').close()
            else:
                path = os.path.join(self.base_path, line.rstrip('/'))
                os.makedirs(path, exist_ok=True)