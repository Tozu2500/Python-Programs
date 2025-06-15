import sys
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QTextEdit, QVBoxLayout,
                            QWidget, QMenuBar, QAction, QFileDialog, QMessageBox,
                            QHBoxLayout, QLabel, QStatusBar, QFontDialog,
                            QColorDialog, QToolBar)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont, QIcon, QKeySequence, QTextCursor

class Notepad(QMainWindow):
    def __init__(self):
        super().__init__()
        