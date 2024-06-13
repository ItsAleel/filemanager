from PyQt6.QtCore import QThread, pyqtSignal
import os

class SearchThread(QThread):
    search_complete = pyqtSignal(list)

    def __init__(self, root_path: str, search_text: str):
        super().__init__()
        self.root_path = root_path
        self.search_text = search_text

    def run(self):
        matches = []
        for root, dirs, files in os.walk(self.root_path):
            for name in dirs + files:
                if self.search_text.lower() in name.lower():
                    matches.append(os.path.join(root, name))
        self.search_complete.emit(matches)
