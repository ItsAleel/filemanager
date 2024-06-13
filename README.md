# File Manager with AI Assist

## Table of Contents

1. [Overview](#overview)
2. [Features](#features)
3. [Installation](#installation)
4. [Usage](#usage)
5. [Settings](#settings)
6. [Console Tab](#console-tab)
7. [Contributing](#contributing)
8. [License](#license)
9. [Acknowledgements](#acknowledgements)

## Overview

The File Manager with AI Assist is a robust and intuitive application designed to help you manage your files and directories efficiently. Leveraging PyQt6 for the GUI and integrating AI capabilities via the Groq API, this application not only provides traditional file management features but also offers advanced functionalities such as automated code imports and intelligent file structure creation.

## Features

- **File and Directory Navigation**: Easily navigate through your file system, view files and directories, and perform common operations like opening, deleting, and renaming.
- **Search Functionality**: Quickly find files and directories using the search feature.
- **AI-Assisted Code Import**: Automatically import code into the correct file based on its content using AI assistance.
- **Settings Management**: Configure general settings and manage API keys securely.
- **Console Tab**: View detailed logs and monitor application activities in real-time.

## Installation

### Prerequisites

- Python 3.8+
- Pip (Python package installer)

### Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/file-manager-ai-assist.git
   cd file-manager-ai-assist
   ```

2. **Create and activate a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows, use `venv\Scripts\activate`
   ```

3. **Install the required packages**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   - Create a `.env` file in the `settings/secret/` directory.
   - Add your Groq API key:
     ```
     GROQ_API_KEY=your_api_key_here
     ```

5. **Run the application**:
   ```bash
   python src/main.py
   ```

## Usage

### Main Operations

- **Navigation**: Use the back button, drive selector, and directory input to navigate through your file system.
- **Search**: Enter keywords in the search bar to filter files and directories.
- **Context Menu**: Right-click on a file or directory to access options like open, set as root directory, delete, rename, and import code.

### AI-Assisted Features

- **Import Code**: Right-click in the tree view and select "Import Code" to automatically import code into the appropriate file based on its content. Ensure that the AI Assist functionality is configured correctly.

## Settings

- **General Settings**: Configure general application settings.
- **AI/LLM Settings**: Manage your Groq API key securely.

## Console Tab

- **Logging**: View real-time logs of the application's activities. The console tab provides detailed insights and helps in debugging.

## Contributing

We welcome contributions from the community! To contribute:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/YourFeatureName`).
3. Make your changes.
4. Commit your changes (`git commit -m 'Add some feature'`).
5. Push to the branch (`git push origin feature/YourFeatureName`).
6. Open a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

- **PyQt6**: For providing the GUI framework.
- **Groq**: For the AI assistance capabilities.
