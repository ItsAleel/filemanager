import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QStatusBar, QTabWidget
from main_operations import MainOperations
from settings import Settings
from console_tab import ConsoleTab
from info import InfoTab  # Import InfoTab from the new file

class FileManager(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('File Manager')
        self.setGeometry(100, 100, 1000, 700)

        self.create_status_bar()

        self.tabs = QTabWidget()
        self.console_tab = ConsoleTab(self)  # Initialize the console tab
        self.main_operations = MainOperations(self, self.console_tab)  # Pass console_tab to MainOperations
        self.settings = Settings(self)
        self.info_tab = InfoTab(self)  # Initialize the Info tab

        self.tabs.addTab(self.main_operations, "Main Operations")
        self.tabs.addTab(self.settings, "Settings")
        self.tabs.addTab(self.console_tab, "Console")
        self.tabs.addTab(self.info_tab, "Info")

        self.setCentralWidget(self.tabs)

    def create_status_bar(self):
        status_bar = QStatusBar(self)
        self.setStatusBar(status_bar)

    def log_to_console(self, message):
        self.console_tab.log_message(message)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = FileManager()
    ex.show()
    sys.exit(app.exec())
