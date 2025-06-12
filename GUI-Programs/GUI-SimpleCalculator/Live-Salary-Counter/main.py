import sys
import os
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from gui.main_window import SalaryCounterWindow
from utils.config import Config

def main():
    app = QApplication(sys.argv)

    # App properties
    app.setApplicationName("Salary counter - Real time")
    app.setApplicationVersion("1.0 Final")
    app.setOrganizationName("Tozu - Tomi Louhiniitty")

    # Set default font
    font = QFont("Segoe UI", 10)
    app.setFont(font)

    # Enabling high DPI scaling
    app.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    app.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

    # Load configuration
    config = Config()

    # Create and make the main window visible
    window = SalaryCounterWindow(config)
    window.show()

    # Run the app
    sys.exit(app.exec_())

if __name__ == '__name__':
    main()