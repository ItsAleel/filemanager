from PyQt6.QtCore import QSortFilterProxyModel, Qt, QThread, pyqtSignal, pyqtSlot
import os

class SearchFilterProxyModel(QSortFilterProxyModel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFilterCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.setFilterKeyColumn(0)

    @pyqtSlot(str)
    def set_filter(self, text):
        if not text:
            self.setFilterRegularExpression("")
        else:
            self.setFilterRegularExpression(f".*{text}.*")

class SearchThread(QThread):
    search_complete = pyqtSignal(list)

    def __init__(self, root_path, search_text):
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
