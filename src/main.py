import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QMenuBar, QStatusBar, QTabWidget
from main_operations import MainOperations
from settings import Settings

class FileManager(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('File Manager')
        self.setGeometry(100, 100, 1000, 700)

        self.create_menu_bar()
        self.create_status_bar()

        self.tabs = QTabWidget()
        self.tabs.addTab(MainOperations(self), "Main Operations")
        self.tabs.addTab(Settings(self), "Settings")

        self.setCentralWidget(self.tabs)

    def create_menu_bar(self):
        menu_bar = QMenuBar(self)

        file_menu = menu_bar.addMenu('File')
        edit_menu = menu_bar.addMenu('Edit')
        view_menu = menu_bar.addMenu('View')
        help_menu = menu_bar.addMenu('Help')

        self.setMenuBar(menu_bar)

    def create_status_bar(self):
        status_bar = QStatusBar(self)
        self.setStatusBar(status_bar)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = FileManager()
    ex.show()
    sys.exit(app.exec())
