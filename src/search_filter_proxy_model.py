# src/search_filter_proxy_model.py

from PyQt6.QtCore import QSortFilterProxyModel, Qt

class SearchFilterProxyModel(QSortFilterProxyModel):
    def __init__(self):
        super().__init__()
        self.setFilterCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.setFilterKeyColumn(0)

    def set_filter(self, text: str):
        if not text:
            self.setFilterRegularExpression("")
        else:
            self.setFilterRegularExpression(f".*{text}.*")
