# src/core/settings.py

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QMessageBox, QTabWidget, QGroupBox, QFormLayout, QHBoxLayout)
from PyQt6.QtGui import QIcon
import json
import os
from dotenv import load_dotenv, set_key

# Constants for file paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SETTINGS_DIR = os.path.join(BASE_DIR, '../settings')
SECRET_ENV_DIR = os.path.join(BASE_DIR, '../settings/secret')
SETTINGS_FILE = os.path.join(SETTINGS_DIR, 'settings.json')
SECRET_ENV_FILE = os.path.join(SECRET_ENV_DIR, '.env')

class GeneralSettingsTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.load_settings()

    def setup_ui(self):
        self.layout = QVBoxLayout(self)
        self.general_group = QGroupBox("General Settings")
        self.general_layout = QFormLayout()

        self.general_setting_input = QLineEdit(self)
        self.general_setting_input.setPlaceholderText("Enter a general setting...")
        self.general_layout.addRow(QLabel("General Setting:"), self.general_setting_input)

        self.general_group.setLayout(self.general_layout)
        self.layout.addWidget(self.general_group)

        self.buttons_layout = QHBoxLayout()
        self.save_button = QPushButton("Save Settings")
        self.save_button.setIcon(QIcon.fromTheme("document-save"))
        self.save_button.clicked.connect(self.save_settings)
        self.buttons_layout.addWidget(self.save_button)

        self.load_button = QPushButton("Load Settings")
        self.load_button.setIcon(QIcon.fromTheme("document-open"))
        self.load_button.clicked.connect(self.load_settings)
        self.buttons_layout.addWidget(self.load_button)

        self.layout.addLayout(self.buttons_layout)
        self.setLayout(self.layout)

    def save_settings(self):
        settings = {
            'general_setting': self.general_setting_input.text(),
        }
        try:
            os.makedirs(os.path.dirname(SETTINGS_FILE), exist_ok=True)
            with open(SETTINGS_FILE, 'w') as f:
                json.dump(settings, f)
                f.flush()
                os.fsync(f.fileno())
            QMessageBox.information(self, "Settings Saved", "Settings have been saved successfully.")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"An error occurred while saving settings: {str(e)}")

    def load_settings(self):
        errors = []
        try:
            if not os.path.exists(SETTINGS_FILE):
                os.makedirs(os.path.dirname(SETTINGS_FILE), exist_ok=True)
                with open(SETTINGS_FILE, 'w') as f:
                    json.dump({}, f)
            with open(SETTINGS_FILE, 'r') as f:
                settings = json.load(f)
            self.general_setting_input.setText(settings.get('general_setting', ''))
        except Exception as e:
            errors.append(f"An error occurred while loading settings: {str(e)}")

        if errors:
            QMessageBox.warning(self, "Error", "\n".join(errors))

class AiSettingsTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.load_api_key()

    def setup_ui(self):
        self.layout = QVBoxLayout(self)
        self.ai_group = QGroupBox("AI/LLM Settings")
        self.ai_layout = QFormLayout()

        self.api_key_input = QLineEdit(self)
        self.api_key_input.setPlaceholderText("Enter Groq API key...")
        self.api_key_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.ai_layout.addRow(QLabel("Groq API Key:"), self.api_key_input)

        self.ai_group.setLayout(self.ai_layout)
        self.layout.addWidget(self.ai_group)

        self.buttons_layout = QHBoxLayout()
        self.save_button = QPushButton("Save API Key")
        self.save_button.setIcon(QIcon.fromTheme("document-save"))
        self.save_button.clicked.connect(self.save_api_key)
        self.buttons_layout.addWidget(self.save_button)

        self.load_button = QPushButton("Load API Key")
        self.load_button.setIcon(QIcon.fromTheme("document-open"))
        self.load_button.clicked.connect(self.load_api_key)
        self.buttons_layout.addWidget(self.load_button)

        self.layout.addLayout(self.buttons_layout)
        self.setLayout(self.layout)

    def save_api_key(self):
        api_key = self.api_key_input.text()
        try:
            os.makedirs(os.path.dirname(SECRET_ENV_FILE), exist_ok=True)
            with open(SECRET_ENV_FILE, 'w') as f:
                f.write(f'GROQ_API_KEY={api_key}\n')
                f.flush()
                os.fsync(f.fileno())
            QMessageBox.information(self, "API Key Saved", "API key has been saved successfully.")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"An error occurred while saving the API key: {str(e)}")

    def load_api_key(self):
        errors = []
        try:
            if not os.path.exists(SECRET_ENV_FILE):
                os.makedirs(os.path.dirname(SECRET_ENV_FILE), exist_ok=True)
                with open(SECRET_ENV_FILE, 'w') as f:
                    f.write('')
            load_dotenv(SECRET_ENV_FILE)
            api_key = os.getenv('GROQ_API_KEY', '')
            self.api_key_input.setText(api_key)
            if not api_key:
                errors.append("No API key found in the .env file.")
        except Exception as e:
            errors.append(f"An error occurred while loading the API key: {str(e)}")

        if errors:
            QMessageBox.warning(self, "Error", "\n".join(errors))

class Settings(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        self.layout = QVBoxLayout(self)
        self.tabs = QTabWidget()

        self.general_settings_tab = GeneralSettingsTab(self)
        self.ai_settings_tab = AiSettingsTab(self)

        self.tabs.addTab(self.general_settings_tab, "General")
        self.tabs.addTab(self.ai_settings_tab, "AI/LLM")

        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)
