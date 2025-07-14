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
    
    @staticmethod
    def create_progress_bar(label: str, value: float) -> QWidget:
        # Progress bar with a label
        row = QWidget()
        layout = QHBoxLayout()

        label_widget = QLabel(f"{label}:")
        label_widget.setMinimumWidth(150)

        progress = QProgressBar()
        progress.setValue(int(value))
        progress.setFormat(f"{value:.1f}%")

        layout.addWidget(label_widget)
        layout.addWidget(progress)

        row.setLayout(layout)
        return row
    
    @staticmethod
    def create_info_frame(title: str) -> tuple:
        # A frame with title for info grouping
        frame = QFrame()
        frame.setFrameStyle(QFrame.Box)
        frame_layout = QVBoxLayout()

        if title:
            title_label = QLabel(title)
            title_label.setStyleSheet("font-weight: bold; margin-bottom: 5px")
            frame_layout.addWidget(title_label)

        frame.setLayout(frame_layout)
        return frame, frame_layout
    
    @staticmethod
    def clear_layout(layout):
        # Clear all widgets
        for i in reversed(range(layout.count())):
            layout.itemAt(i).widget().setParent(None)
