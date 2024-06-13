from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QScrollBar
from PyQt6.QtCore import QMutex, QMutexLocker, QThread, pyqtSignal, pyqtSlot

class ConsoleTab(QWidget):
    log_signal = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.console = QTextEdit(self)
        self.console.setReadOnly(True)
        self.layout.addWidget(self.console)
        self.setLayout(self.layout)
        self.log_signal.connect(self.append_log)
        self.mutex = QMutex()

    def log_message(self, message):
        self.log_signal.emit(message)

    @pyqtSlot(str)
    def append_log(self, message):
        with QMutexLocker(self.mutex):
            self.console.append(message)
            scroll_bar = self.console.verticalScrollBar()
            scroll_bar.setValue(scroll_bar.maximum())
