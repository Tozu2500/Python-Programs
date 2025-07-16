import random
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QSpinBox, QTextEdit
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont, QPalette

class DiceGame(QWidget):
    def __init__(self, stats_manager, return_callback):
        super().__init__()
        self.stats_manager = stats_manager
        self.return_callback = return_callback
        self.roll_history = []
        self.current_session_rolls = 0
        self.animation_timer = QTimer()
        self.animation_timer.timeout.connect(self.animate_roll)
        self.animation_count = 0
        self.final_result = None
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Title
        title = QLabel("Dice roller game")
        title.setFont(QFont("Arial", 20, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Dice count selector
        dice_layout = QHBoxLayout()
        dice_layout.addWidget(QLabel("Number of dice:"))
        self.dice_count = QSpinBox()
        self.dice_count.setMinimum(1)
        self.dice_count.setMaximum(6)
        self.dice_count.setValue(2)
        dice_layout.addWidget(self.dice_count)
        dice_layout.addStretch()

        dice_widget = QWidget()
        dice_widget.setLayout(dice_layout)
        layout.addWidget(dice_widget)

        # Result display
        self.result_label = QLabel("Click 'Roll Dice' to start!")
        self.result_label.setFont(QFont("Arial", 16))
        self.result_label.setAlignment(Qt.AlignCenter)
        self.result_label.setStyleSheet("border: 2px solid #333; padding: 20px; margin: 10px;")
        layout.addWidget(self.result_label)

        # Rolling button
        self.roll_button = QPushButton("Roll Dice")
        self.roll_button.setFont(QFont("Arial", 14))
        self.roll_button.clicked.connect(self.start_roll_animation)
        layout.addWidget(self.roll_button)

        # Stats display
        self.stats_label = QLabel()
        self.stats_label.setFont(QFont("Arial", 10))
        self.update_stats_display()
        layout.addWidget(self.stats_label)

        # Rolling history
        history_label = QLabel("Roll History (this session):")
        history_label.setFont(QFont("Arial", 12, QFont.Bold))
        layout.addWidget(history_label)

        self.history_text = QTextEdit()
        self.history_text.setMaximumHeight(150)
        self.history_text.setReadOnly(True)
        layout.addWidget(self.history_text)

        # Control buttons
        button_layout = QHBoxLayout()

        clear_btn = QPushButton("Clear History")
        clear_btn.clicked.connect(self.clear_history)
        button_layout.addWidget(clear_btn)

        back_btn = QPushButton("Back to Menu")
        back_btn.clicked.connect(self.return_callback)
        button_layout.addWidget(back_btn)

        button_widget = QWidget()
        button_widget.setLayout(button_layout)
        layout.addWidget(button_widget)

        self.setLayout(layout)

    def start_roll_animation(self):
        self.roll_button.setEnabled(False)
        self.animation_count = 0

        # Final result
        num_dice = self.dice_count.value()
        self.final_result = [random.randint(1, 6) for _ in range(num_dice)]

        # Animation start
        self.animation_timer.start(100) # 100ms intervals

    def animate_roll(self):
        self.animation_count += 1

        if self.animation_count < 10: # 1 second anim
            # Show random nums during animation
            num_dice = self.dice_count.value()
            temp_result = [random.randint(1, 6) for _ in range(num_dice)]
            self.display_result(temp_result, is_final=False)
        else:
            # Final result
            self.animation_timer.stop()
            self.display_result(self.final_result, is_final=True)
            self.roll_button.setEnabled(True)

    def display_button(self, dice_values, is_final=True):
        if is_final:
            # Record roll
            self.record_roll(dice_values)

        # Create text
        total = sum(dice_values)
        dice_str = " + ".join(map(str, dice_values))

        if len(dice_values) == 1:
            result_text = f"🎲 {dice_values[0]}"
        else:
            result_text = f"🎲 {dice_str} = {total}"

        if not is_final:
            result_text += " (rolling...)"

        self.result_label.setText(result_text)

        # Color codes for final results
        if is_final:
            if total == len(dice_values):
                self.result_label.setStyleSheet("border: 2px solid #d32f2f; padding: 20px; margin: 10px; color: #d32f2f;")
            elif total == len(dice_values) * 6:
                self.result_label.setStyleSheet("border: 2px solid #388e3c; padding: 20px; margin: 10px; color: #388e3c;")
            else:
                self.result_label.setStyleSheet("border: 2px solid #333; padding: 20px; margin: 10px; color: black;")

    def record_roll(self, dice_values):
        self.current_session_rolls += 1

        # Add to history
        total = sum(dice_values)
        if len(dice_values) == 1:
            history_entry = f"Roll {self.current_session_rolls}: {dice_values[0]}"
        else:
            dice_str = " + ".join(map(str, dice_values))
            history_entry = f"Roll {self.current_session_rolls}: {dice_str} = {total}"

        self.roll_history.append(history_entry)

        # Update history display
        self.history_text.clear()
        # Show last ten rolls
        recent_history = self.roll_history[-10:]
        self.history_text.setText("\n".join(recent_history))

        # Update stats
        self.stats_manager.record_dice_roll(dice_values)
        self.update_stats_display()

    def update_stats_display(self):
        stats = self.stats_manager.get_dice_stats()
        stats_text = f"Session rolls: {self.current_session_rolls} | "
        stats_text += f"Total rolls: {stats.get('total_rolls', 0)} | "
        stats_text += f"Games played: {stats.get('games_played', 0)}"
        self.stats_label.setText(stats_text)

    def clear_history(self):
        self.roll_history.clear()
        self.current_session_rolls = 0
        self.history_text.clear()
        self.result_label.setText("Click 'Roll Dice' to start!")
        self.result_label.setStyleSheet("border: 2px solid #333; padding: 20px; margin: 10px; color: black;")

        # Record new game session
        self.stats_manager.record_dice_game()
        self.update_stats_display()

    def showEvent(self):
        super().showEvent(event)
        self.update_stats_display()
