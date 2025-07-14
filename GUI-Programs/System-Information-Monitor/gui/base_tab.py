# Base tab - For system info tabs
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QScrollArea
from gui.components import ComponentFactory

class BaseTab(QWidget):
    # Base class for all system info tabs

    def __init__(self, title: str):
        super().__init__()
        self.title = title
        self.setup_ui()

    def setup_ui(self):
        # Basic UI structure
        self.main_layout = QVBoxLayout()

        # Scroll area
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)

        # Content widget
        self.content = QWidget()
        self.content_layout = QVBoxLayout()
        self.content.setLayout(self.content_layout)

        # Set scroll widget
        self.scroll.setWidget(self.content)

        # Add to main layout
        self.main_layout.addWidget(self.scroll)
        self.setLayout(self.main_layout)

    def add_section(self, title: str):
        # Add a section with header
        header = ComponentFactory.create_section_header(title)
        self.content_layout.addWidget(header)
        return header
    
    def add_info_row(self, label: str, value: str):
        # Add info row
        row = ComponentFactory.create_info_row(label, value)
        self.content_layout.addWidget(row)
        return row
    
    def add_progress_bar(self, label: str, value: float):
        # Add progress bar
        bar = ComponentFactory.create_progress_bar(label, value)
        self.content_layout.addWidget(bar)
        return bar
    
    def add_widget(self, widget):
        # Add a widget to the content layout
        self.content_layout.addWidget(widget)

    def clear_content(self):
        # Clear all content from the tab
        ComponentFactory.clear_layout(self.content_layout)

    def update_content(self):
        # Override this method to update tab content
        pass
    
