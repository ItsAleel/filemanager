from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QScrollBar, QLineEdit, QPushButton, QFileDialog, QComboBox, QMenu
from PyQt6.QtCore import QMutex, QMutexLocker, QThread, pyqtSignal, pyqtSlot, Qt
from datetime import datetime

class ConsoleTab(QWidget):
    log_signal = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)

        # Search bar
        self.search_bar = QLineEdit(self)
        self.search_bar.setPlaceholderText("Search...")
        self.search_bar.textChanged.connect(self.search_logs)
        self.layout.addWidget(self.search_bar)

        # Console text area
        self.console = QTextEdit(self)
        self.console.setReadOnly(True)
        self.layout.addWidget(self.console)

        # Clear console button
        self.clear_button = QPushButton("Clear Console", self)
        self.clear_button.clicked.connect(self.clear_console)
        self.layout.addWidget(self.clear_button)

        # Save logs button
        self.save_button = QPushButton("Save Logs", self)
        self.save_button.clicked.connect(self.save_logs)
        self.layout.addWidget(self.save_button)

        # Log level filter
        self.log_level_filter = QComboBox(self)
        self.log_level_filter.addItems(["ALL", "INFO", "WARNING", "ERROR"])
        self.log_level_filter.currentTextChanged.connect(self.filter_logs)
        self.layout.addWidget(self.log_level_filter)

        self.setLayout(self.layout)
        self.log_signal.connect(self.append_log)
        self.mutex = QMutex()
        self.all_logs = []  # Store all logs for filtering

        # Add context menu
        self.console.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.console.customContextMenuRequested.connect(self.open_context_menu)

    def log_message(self, message, level="INFO"):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] [{level}] {message}"
        self.all_logs.append(log_entry)
        self.log_signal.emit(log_entry)

    @pyqtSlot(str)
    def append_log(self, message):
        with QMutexLocker(self.mutex):
            self.console.append(message)
            scroll_bar = self.console.verticalScrollBar()
            scroll_bar.setValue(scroll_bar.maximum())

    def search_logs(self, text):
        filtered_logs = [log for log in self.all_logs if text.lower() in log.lower()]
        self.console.clear()
        self.console.append("\n".join(filtered_logs))

    def clear_console(self):
        with QMutexLocker(self.mutex):
            self.console.clear()
            self.all_logs.clear()

    def save_logs(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self, "Save Logs", "", "Text Files (*.txt);;All Files (*)", options=options)
        if file_name:
            with open(file_name, 'w', encoding='utf-8') as file:
                file.write("\n".join(self.all_logs))

    def filter_logs(self, level):
        if level == "ALL":
            filtered_logs = self.all_logs
        else:
            filtered_logs = [log for log in self.all_logs if f"[{level}]" in log]
        self.console.clear()
        self.console.append("\n".join(filtered_logs))

    def open_context_menu(self, position):
        menu = QMenu()
        copy_action = menu.addAction("Copy")
        action = menu.exec(self.console.mapToGlobal(position))
        if action == copy_action:
            self.console.copy()
