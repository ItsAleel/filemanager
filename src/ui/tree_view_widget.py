# src/ui/tree_view_widget.py

import os
from PyQt6.QtWidgets import QTreeView, QVBoxLayout, QWidget, QMenu, QInputDialog, QMessageBox, QLineEdit, QProgressBar
from PyQt6.QtCore import QDir, Qt, pyqtSignal
from PyQt6.QtGui import QCursor, QAction, QFileSystemModel
from utils.search_thread import SearchThread

class TreeViewWidget(QWidget):
    file_double_clicked = pyqtSignal(str)
    dir_changed = pyqtSignal(str)
    file_selected = pyqtSignal(str)
    directory_selected = pyqtSignal(str)  # New signal for directory selection

    def __init__(self, parent=None, ai_assist=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        
        self.model = QFileSystemModel()
        self.model.setRootPath(QDir.rootPath())
        self.model.setFilter(QDir.Filter.AllEntries | QDir.Filter.NoDotAndDotDot)
        
        self.tree = QTreeView()
        self.tree.setModel(self.model)
        self.tree.setRootIndex(self.model.index(QDir.rootPath()))
        self.tree.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.tree.customContextMenuRequested.connect(self.open_context_menu)
        self.tree.doubleClicked.connect(self.on_double_click)
        self.tree.selectionModel().selectionChanged.connect(self.on_selection_changed)
        self.tree.setColumnHidden(1, True)
        self.tree.setColumnHidden(2, True)
        self.tree.setColumnHidden(3, True)

        self.progress_bar = QProgressBar(self)
        self.progress_bar.setVisible(False)

        self.layout.addWidget(self.tree)
        self.layout.addWidget(self.progress_bar)
        self.setLayout(self.layout)

        self.search_thread = None
        self.ai_assist = ai_assist
        self.current_directory = QDir.rootPath()  # Track the current directory

    def setModel(self, model):
        self.tree.setModel(model)

    def set_root_directory(self, path):
        if os.path.exists(path):
            self.current_directory = path  # Update the current directory
            self.model.setRootPath(path)
            self.tree.setRootIndex(self.model.index(path))
            self.dir_changed.emit(path)

    def on_double_click(self, index):
        path = self.model.filePath(index)
        if os.path.isdir(path):
            self.set_root_directory(path)
        elif os.path.isfile(path):
            self.file_double_clicked.emit(path)

    def on_selection_changed(self, selected, deselected):
        indexes = self.tree.selectionModel().selectedIndexes()
        if indexes:
            path = self.model.filePath(indexes[0])
            if os.path.isdir(path):
                self.directory_selected.emit(path)  # Emit directory path
            elif os.path.isfile(path):
                self.file_selected.emit(path)

    def open_context_menu(self, position):
        indexes = self.tree.selectedIndexes()
        if indexes:
            menu = QMenu()
            open_action = QAction("Open", self)
            open_action.triggered.connect(lambda: self.on_double_click(indexes[0]))
            menu.addAction(open_action)
            set_as_current_dir_action = QAction("Set as Root Directory", self)
            set_as_current_dir_action.triggered.connect(lambda: self.set_root_directory(self.model.filePath(indexes[0])))
            menu.addAction(set_as_current_dir_action)
            delete_action = QAction("Delete", self)
            delete_action.triggered.connect(lambda: self.delete_item(indexes[0]))
            menu.addAction(delete_action)
            rename_action = QAction("Rename", self)
            rename_action.triggered.connect(lambda: self.rename_item(indexes[0]))
            menu.addAction(rename_action)
            import_code_action = QAction("Import Code", self)
            import_code_action.triggered.connect(self.import_code)
            menu.addAction(import_code_action)
            menu.exec(QCursor.pos())

    def delete_item(self, index):
        path = self.model.filePath(index)
        reply = QMessageBox.question(self, "Delete", f"Are you sure you want to delete {path}?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            try:
                if os.path.isdir(path):
                    os.rmdir(path)
                else:
                    os.remove(path)
                QMessageBox.information(self, "Deleted", f"{path} has been deleted.")
                self.model.setRootPath(self.model.rootPath())
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Could not delete {path}. Error: {e}")

    def rename_item(self, index):
        path = self.model.filePath(index)
        new_name, ok = QInputDialog.getText(self, "Rename", "Enter new name:", QLineEdit.Normal, QDir(path).dirName())
        if ok and new_name:
            new_path = os.path.join(os.path.dirname(path), new_name)
            try:
                os.rename(path, new_path)
                QMessageBox.information(self, "Renamed", f"{path} has been renamed to {new_name}.")
                self.model.setRootPath(self.model.rootPath())
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Could not rename {path}. Error: {e}")

    def start_search(self, root_path, search_text):
        if self.search_thread and self.search_thread.isRunning():
            self.search_thread.terminate()

        self.progress_bar.setVisible(True)
        self.search_thread = SearchThread(root_path, search_text)
        self.search_thread.search_complete.connect(self.on_search_complete)
        self.search_thread.start()

    def on_search_complete(self, matches):
        self.progress_bar.setVisible(False)
        print("Search complete:", matches)

    def import_code(self):
        if self.ai_assist:
            code = self.get_code_to_import()
            if code:
                self.ai_assist.set_current_directory(self.current_directory)
                self.ai_assist.ai_import_code_into_file(code, self.current_directory)
        else:
            QMessageBox.warning(self, "AI Assist Not Available", "AI Assist functionality is not available.")

    def get_code_to_import(self):
        # This method should get the code to be imported from an appropriate source, e.g., a text editor.
        # For this example, we'll just return a sample code string.
        return "def example_function():\n    print('Hello, World!')"
