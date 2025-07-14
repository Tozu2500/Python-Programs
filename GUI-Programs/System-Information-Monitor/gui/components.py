# Reusable gui components made here
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                            QProgressBar, QFrame)
from PyQt5.QtCore import Qt

class ComponentFactory:
    @staticmethod
    def create_section_header(title: str) -> QLabel:
        # Create styled section header
        header = QLabel(title)
        header.setStyleSheet("""
            font-size: 14px;
            font-weight: bold;
            color: #333;
            padding: 5px;
            background-color: #e8f4f8;
            border-radius: 4px;                     
        """)
        return header
    
    @staticmethod
    def create_info_row(label: str, value: str) -> QWidget:
        # Info row with a label and a value
        row = QWidget()
        layout = QHBoxLayout()

        label_widget = QLabel(f"{label}")
        label_widget.setMinimumWidth(150)

        value_widget = QLabel(str(value))
        value_widget.setStyleSheet("""
            font-family: 'Courier New', monospace;
            background-color: #f8f8f8;
            padding: 2px 4px;
            border-radius: 2px;
        """)

        layout.addWidget(label_widget)
        layout.addWidget(value_widget)

        row.setLayout(layout)
        return row