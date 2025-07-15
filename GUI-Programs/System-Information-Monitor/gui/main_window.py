# Main window for system info monitor
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QTabWidget
from PyQt5.QtCore import QTimer
from gui.tabs import OverviewTab, CPUTab, MemoryTab, DiskTab, NetworkTab, ProcessesTab

class SystemInfoApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("System info monitor")
        self.setGeometry(100, 100, 900, 700)

        # Central widget + main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Creating tab widget
        self.tabs = QTabWidget()
        layout = QVBoxLayout()
        layout.addWidget(self.tabs)
        central_widget.setLayout(layout)

        # Creating and adding the tabs
        self.overview_tab = OverviewTab()
        self.cpu_tab = CPUTab()
        self.memory_tab = MemoryTab()
        self.disk_tab = DiskTab()
        self.network_tab = NetworkTab()
        self.processes_tab = ProcessesTab()

        self.tabs.addTab(self.overview_tab, "Overview")
        self.tabs.addTab(self.cpu_tab, "CPU")
        self.tabs.addTab(self.memory_tab, "Memory")
        self.tabs.addTab(self.disk_tab, "Disk")
        self.tabs.addTab(self.network_tab, "Network")
        self.tabs.addTab(self.processes_tab, "Processes")

        # Storing tabs for easy iterations
        self.dynamic_tabs = [
            self.overview_tab,
            self.cpu_tab,
            self.memory_tab,
            self.disk_tab,
            self.network_tab
        ]

        # Set up a timer for real-time updates
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_dynamic_info)
        self.timer.start(2000) # 2-second intervals

        self.apply_styling()

        self.update_dynamic_info()

    def apply_styling(self):
        # Apply app styles
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f0f0;               
            }
            QTabWidget::pane {
                border: 1px solid #c0c0c0;
                background-color: white;               
            }
            QTabBar::tab {
                background-color: #e0e0e0;               
            }
            QTabBar::tab:selected {
                background-color: #4CAF50;
                color: white;               
            }
            QLabel {
                font-size: 12px;        
            }
        """)

    def update_dynamic(self):
        for tab in self.dynamic_tabs:
            tab.update_content()
