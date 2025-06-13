
# Input widget for salary config
# Handles user input for salary amount and takes the user input for the time frame

from PyQt5.QtWidgets import (QWidget, QVboxLayout, QHBoxLayout, QLabel,
                             QLineEdit, QComboBox, QPushButton, QFrame,
                             QMessageBox)
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QDoubleValidator

class SalaryInputWidget(QWidget):
    # Input salary information

    salary_configured = pyqtSignal(float, str)

    def __init__(self, config):
        super().__init__()
        self.config = config
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(15)

        title = QLabel("Count your salary - LIVE")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        input_frame = QFrame()
        input_layout = QVboxLayout(input_frame)

        # Salary input
        salary_layout = QHBoxLayout()
        salary_label = QLabel("Enter salary amount: ")
        self.salary_input = QLineEdit()
        self.salary_input.setPlaceholderText("Enter your salary amount and select a time frame...")

        validator = QDoubleValidator()
        validator.setDecimals(4)
        validator.setNotation(QDoubleValidator.StandardNotation)
        self.salary_input.setValidator(validator)

        salary_layout.addWidget(salary_label)
        salary_layout.addWidget(self.salary_input)
        input_layout.addLayout(salary_layout)

        # Time frame selection
        timeframe_layout = QHBoxLayout()
        timeframe_label = QLabel("Time frame: ")
        self.timeframe_combo = QComboBox()
        self.timeframe_combo.addItems(["Hour", "Day", "Week", "Month", "Year"])
        self.timeframe_combo.setCurrentText("Year")

        timeframe_layout.addWidget(timeframe_label)
        timeframe_layout.addWidget(self.timeframe_combo)
        input_layout.addLayout(timeframe_layout)

        # Example text
        self.example_label = QLabel("Example: Enter 50 000 (No matter the currency) = 24.04 (Currency) per hour")
        self.example_label.setObjectName("info")
        self.example_label.setAlignment(Qt.AlignCenter)
        input_layout.addWidget(self.example_label)

        layout.addWidget(input_frame)

        # Buttons
        button_layout = QHBoxLayout()

        self.start_button = QPushButton("Start the counter!")
        self.start_button.setObjectName("primary")
        self.start_button.clicked.connect(self.start_counter)

        self.clear_button = QPushButton("Clear")
        self.clear_button.clicked.connect(self.clear_inputs)

        button_layout.addWidget(self.clear_button)
        button_layout.addWidget(self.start_button)

        layout.addLayout(button_layout)

        # Connect signals for real-time updating
        self.salary_input.textChanged.connect(self.update_example)
        self.timeframe_combo.currentTextChanged.connect(self.update_example)

        self.setLayout(layout)
        self.update_example()

    def update_example(self):
        try:
            salary_text = self.salary_input.text()
            if not salary_text:
                self.example_label.setText("Enter a salary amount to calculate")
                return
            
            salary = float(salary_text)
            timeframe = self.timeframe_combo.currentText()

            # Calculating the hourly rate for example
            multipliers = self.config.time_multipliers
            hours_per_timeframe = multipliers[timeframe] / 3600 # Hour converting
            hourly_rate = salary / hours_per_timeframe

            self.example_label.setText(
                f"${salary:,.0f} per {timeframe} = ${hourly_rate:.2f} per hour"
            )
        
        except (ValueError, ZeroDivisionError):
            self.example_label.setText("Enter a valid salary number!")

    def start_counter(self):
        """Validate input and start the counter"""
        salary_text = self.salary_input.text()
        
        if not salary_text:
            self.show_error("Please enter a salary amount")
            return
        
        try:
            salary = float(salary_text)
            if salary <= 0:
                self.show_error("Salary amount must be greater than 0")
                return
            
            timeframe = self.timeframe_combo.currentText()
            self.salary_configured.emit(salary, timeframe)
            
        except ValueError:
            self.show_error("Please enter a valid salary amount")
        
    def clear_inputs(self):
        self.salary_input.clear()
        self.timeframe_combo.setCurrentText("Year")
        self.update_example()

    def show_error(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowTitle("Input value error")
        msg.setText(message)
        msg.exec_()

    def get_current_values(self):
        try:
            salary = float(self.salary_input.text()) if self.salary_input.text() else 0
            timeframe = self.timeframe_combo.currentText()
            return salary, timeframe
        except ValueError:
            return 0, "Year"

