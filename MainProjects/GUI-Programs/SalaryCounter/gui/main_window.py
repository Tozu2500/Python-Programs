"""
Main window for the Salary Counter application.
"""

from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QLineEdit, QComboBox, QPushButton, QFrame)
from PyQt5.QtCore import QTimer, Qt, pyqtSignal
from PyQt5.QtGui import QFont, QPalette, QColor
from core.salary_calculator import SalaryCalculator, TimeFrame
from gui.styles import StyleSheet


class MainWindow(QMainWindow):
    """Main application window containing all UI elements."""
    
    def __init__(self):
        super().__init__()
        self.salary_calculator = None
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_counter)
        
        self.init_ui()
        self.apply_styles()
    
    def init_ui(self):
        """Initialize the user interface."""
        self.setWindowTitle("Real-time Salary Counter")
        self.setGeometry(100, 100, 600, 400)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(40, 40, 40, 40)
        
        # Title
        self.title_label = QLabel("💰 Real-time Salary Counter")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setObjectName("title")
        main_layout.addWidget(self.title_label)
        
        # Input section
        input_frame = QFrame()
        input_frame.setObjectName("inputFrame")
        input_layout = QVBoxLayout(input_frame)
        
        # Salary input row
        salary_row = QHBoxLayout()
        salary_label = QLabel("Salary:")
        salary_label.setObjectName("inputLabel")
        self.salary_input = QLineEdit()
        self.salary_input.setPlaceholderText("Enter your salary amount")
        self.salary_input.setObjectName("salaryInput")
        
        salary_row.addWidget(salary_label)
        salary_row.addWidget(self.salary_input)
        input_layout.addLayout(salary_row)
        
        # Timeframe selection row
        timeframe_row = QHBoxLayout()
        timeframe_label = QLabel("Timeframe:")
        timeframe_label.setObjectName("inputLabel")
        self.timeframe_combo = QComboBox()
        self.timeframe_combo.setObjectName("timeframeCombo")
        
        # Add timeframe options
        timeframe_options = [
            ("Hourly", TimeFrame.HOURLY),
            ("Daily", TimeFrame.DAILY),
            ("Weekly", TimeFrame.WEEKLY),
            ("Monthly", TimeFrame.MONTHLY),
            ("Yearly", TimeFrame.YEARLY)
        ]
        
        for display_text, timeframe_value in timeframe_options:
            self.timeframe_combo.addItem(display_text, timeframe_value)
        
        timeframe_row.addWidget(timeframe_label)
        timeframe_row.addWidget(self.timeframe_combo)
        input_layout.addLayout(timeframe_row)
        
        main_layout.addWidget(input_frame)
        
        # Control buttons
        button_layout = QHBoxLayout()
        
        self.start_button = QPushButton("▶ Start Counter")
        self.start_button.setObjectName("startButton")
        self.start_button.clicked.connect(self.start_counter)
        
        self.stop_button = QPushButton("⏸ Stop Counter")
        self.stop_button.setObjectName("stopButton")
        self.stop_button.clicked.connect(self.stop_counter)
        self.stop_button.setEnabled(False)
        
        self.reset_button = QPushButton("🔄 Reset")
        self.reset_button.setObjectName("resetButton")
        self.reset_button.clicked.connect(self.reset_counter)
        
        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.stop_button)
        button_layout.addWidget(self.reset_button)
        main_layout.addLayout(button_layout)
        
        # Counter display
        counter_frame = QFrame()
        counter_frame.setObjectName("counterFrame")
        counter_layout = QVBoxLayout(counter_frame)
        
        counter_title = QLabel("Current Earnings:")
        counter_title.setAlignment(Qt.AlignCenter)
        counter_title.setObjectName("counterTitle")
        
        self.counter_display = QLabel("€0.0000")
        self.counter_display.setAlignment(Qt.AlignCenter)
        self.counter_display.setObjectName("counterDisplay")
        
        counter_layout.addWidget(counter_title)
        counter_layout.addWidget(self.counter_display)
        main_layout.addWidget(counter_frame)
        
        # Status label
        self.status_label = QLabel("Enter your salary and click Start to begin")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setObjectName("statusLabel")
        main_layout.addWidget(self.status_label)
    
    def apply_styles(self):
        """Apply the modern stylesheet to the window."""
        self.setStyleSheet(StyleSheet.get_stylesheet())
    
    def start_counter(self):
        """Start the salary counter."""
        try:
            salary = float(self.salary_input.text())
            if salary <= 0:
                self.status_label.setText("Please enter a valid salary amount")
                return
                
            timeframe = self.timeframe_combo.currentData()
            
            # Create or update calculator
            if self.salary_calculator is None:
                self.salary_calculator = SalaryCalculator(salary, timeframe)
            else:
                self.salary_calculator.update_salary(salary, timeframe)
            
            # Start the counter and timer
            self.salary_calculator.start_counter()
            self.timer.start(50)  # Update every 50ms for smooth animation
            
            # Update UI state
            self.start_button.setEnabled(False)
            self.stop_button.setEnabled(True)
            self.salary_input.setEnabled(False)
            self.timeframe_combo.setEnabled(False)
            
            self.status_label.setText("Counter is running...")
            
        except ValueError:
            self.status_label.setText("Please enter a valid numeric salary")
    
    def stop_counter(self):
        """Stop the salary counter."""
        self.timer.stop()
        
        # Update UI state
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        self.salary_input.setEnabled(True)
        self.timeframe_combo.setEnabled(True)
        
        self.status_label.setText("Counter stopped")
    
    def reset_counter(self):
        """Reset the salary counter."""
        self.timer.stop()
        
        if self.salary_calculator:
            self.salary_calculator.reset_counter()
        
        self.counter_display.setText("€0.0000")
        
        # Update UI state
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        self.salary_input.setEnabled(True)
        self.timeframe_combo.setEnabled(True)
        
        self.status_label.setText("Counter reset - ready to start")
    
    def update_counter(self):
        """Update the counter display with current earnings."""
        if self.salary_calculator:
            current_earnings = self.salary_calculator.get_current_earnings()
            formatted_earnings = SalaryCalculator.format_currency(current_earnings)
            self.counter_display.setText(formatted_earnings)