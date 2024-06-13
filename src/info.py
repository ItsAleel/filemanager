import webbrowser
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QGroupBox
from PyQt6.QtCore import Qt

class InfoTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)

        # Program Version Section
        version_group = QGroupBox("Program Information", self)
        version_layout = QVBoxLayout()

        version_label = QLabel("File Manager with AI Assist\nVersion 1.0.0", self)
        version_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        version_layout.addWidget(version_label)
        version_group.setLayout(version_layout)
        layout.addWidget(version_group)

        # Links Section
        links_group = QGroupBox("Useful Links", self)
        links_layout = QVBoxLayout()

        github_button = QPushButton("GitHub Repository", self)
        github_button.clicked.connect(self.open_github_link)
        links_layout.addWidget(github_button)

        coffee_button = QPushButton("Support via BuyMeACoffee", self)
        coffee_button.clicked.connect(self.open_coffee_link)
        links_layout.addWidget(coffee_button)

        links_group.setLayout(links_layout)
        layout.addWidget(links_group)

        # Additional Resources Section
        resources_group = QGroupBox("Additional Resources", self)
        resources_layout = QVBoxLayout()

        documentation_button = QPushButton("Documentation", self)
        documentation_button.clicked.connect(self.open_documentation_link)
        resources_layout.addWidget(documentation_button)

        faq_button = QPushButton("FAQ", self)
        faq_button.clicked.connect(self.open_faq_link)
        resources_layout.addWidget(faq_button)

        resources_group.setLayout(resources_layout)
        layout.addWidget(resources_group)

        

        self.setLayout(layout)

    def open_github_link(self):
        webbrowser.open("https://github.com/ItsAleel/filemanager")

    def open_coffee_link(self):
        webbrowser.open("https://buymeacoffee.com/aleel")

    def open_documentation_link(self):
        webbrowser.open("https://github.com/ItsAleel/filemanager/blob/main/README.md")

    def open_faq_link(self):
        webbrowser.open("https://github.com/ItsAleel/filemanager/issues")
