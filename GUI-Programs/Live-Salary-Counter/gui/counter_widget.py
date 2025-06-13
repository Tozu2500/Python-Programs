# Counter widget, shows live salary earnings with smooth updating

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QPushButton, QFrame, QGridLayout)
from PyQt5.QtCore import QTimer, pyqtSignal, Qt
from PyQt5.QtGui import QFont

class SalaryCounterWidget(QWidget):
    # Signals
    stop_requested = pyqtSignal()
    reset_requested = pyqtSignal()

    def __init__(self, config, calculator):
        super().__init__()
        self.config = config
        self.calculator = calculator
        self.setup_ui()
        self.setup_timer()

    def setup_ui(self):
        # Setup for the UI
        layout = QVBoxLayout()
        layout.setSpacing(20)

        # Title
        title = QLabel("Live Salary Counter")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Counter display frame
        counter_frame = QFrame()
        counter_layout = QVBoxLayout(counter_frame)

        # Main earnings display
        self.earnings_label = QLabel("0.00")
        self.earnings_label.setObjectName("counter")
        self.earnings_label.setAlignment(Qt.AlignCenter)
        counter_layout.addWidget(self.earnings_label)

        # Time elapsed count
        self.time_label = QLabel("Time: 00:00")
        self.time_label.setObjectName("info")
        self.time_label.setAlignment(Qt.AlignCenter)
        counter_layout.addWidget(self.time_label)

        layout.addWidget(counter_frame)

        # Statistics frame
        stats_frame = QFrame()
        stats_layout = QGridLayout(stats_frame)

        # Earnings per second
        stats_layout.addWidget(QLabel("Per Second: "), 0, 0)
        self.per_second_label = QLabel("0.00")
        self.per_second_label.setAlignment(Qt.AlignRight)
        stats_layout.addWidget(self.per_second_label, 0, 1)

        # Earnings per minute
        stats_layout.addWidget(QLabel("Per Minute: "), 1, 0)
        self.per_minute_label = QLabel("0.00")
        self.per_minute_label.setAlignment(Qt.AlignRight)
        stats_layout.addWidget(self.per_minute_label, 1, 1)

        # Earnings per hour
        stats_layout.addWidget(QLabel("Per Hour:"), 2, 0)
        self.per_hour_label = QLabel("0.00")
        self.per_hour_label.setAlignment(Qt.AlignRight)
        stats_layout.addWidget(self.per_hour_label, 2, 1)

        # Original salary
        stats_layout.addWidget(QLabel("Base Salary:"), 3, 0)
        self.base_salary_label = QLabel("0.00")
        self.base_salary_label.setAlignment(Qt.AlignRight)
        stats_layout.addWidget(self.base_salary_label, 3, 1)

        layout.addWidget(stats_frame)

        # Control buttons
        button_layout = QHboxLayout()

        self.pause_button = QPushButton("Pause")
        self.pause_button.clicked.connect(self.toggle_pause)
        
        self.reset_button = QPushButton("Reset")
        self.reset_button.setObjectName("danger")
        self.reset_button.clicked.connect(self.reset_counter)

        self.stop_button = QPushButton("Stop & Configure New")
        self.stop_button.clicked.connect(self.stop_counter)

        button_layout.addWidget(self.pause_button)
        button_layout.addWidget(self.reset_button)
        button_layout.addWidget(self.stop_button)

        layout.addLayout(button_layout)

        self.setLayout(layout)
        self.update_static_info()

    def setup_timer(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_counter)
        self.timer.start(self.config.update_interval)

        # Start
        self.calculator.start()

    def update_counter(self):
        if not self.calculator.is_running:
            return
        
        earnings_info = self.calculator.get_earnings_info()

        # Update main display
        self.earnings_label.setText(earnings_info['formatted_earnings'])
        self.time_label.setText(f"Time: {earnings_info['formatted_time']}")

    def update_static_info(self):
        earnings_per_second = self.calculator.earnings_per_second

        per_minute = earnings_per_second * 60
        per_hour = earnings_per_second * 3600

        # Update the labels
        self.per_second_label.setText(self.calculator.format_currency(earnings_per_second))
        self.per_minute_label.setText(self.calculator.format_currency(per_minute))
        self.per_hour_label.setText(self.calculator.format_currency(per_hour))

        base_salary_text = (f"{self.calculator.format_currency(self.calculator.salary_amount)} "
                            f"per {self.calculator.time_frame}")
        self.base_salary_label.setText(base_salary_text)

    def toggle_pause(self):
        if self.calculator.is_running:
            self.calculator.stop()
            self.pause_button.setText("Resume")
        else:
            # Resume
            import time
            current_time = time.time()
            earnings_info = self.calculator.get_earnings_info()
            elapsed = earnings_info['elapsed_time']

            # Adjust start time
            self.calculator.start_time = current_time - elapsed
            self.calculator.is_running = True
            self.pause_button.setText("Pause")

    def reset_counter(self):
        self.calculator.reset()
        self.calculator.start()
        self.pause_button.setText("Pause")
        self.update_counter()

    def stop_counter(self):
        self.timer.stop()
        self.calculator.stop()
        self.stop_requested.emit()

    def closeEvent(self, event):
        if hasattr(self, 'timer'):
            self.timer.stop()
        super().closeEvent(event)
        

