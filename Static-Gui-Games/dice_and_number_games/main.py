# Dice + Number guessing game in one with a statistics feature
import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                            QHBoxLayout, QPushButton, QLabel, QStackedWidget)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from dice_game import DiceGame
from number_guess_game import NumberGuessGame
from stats_manager import StatsManager

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.stats_manager = StatsManager()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Dice roller & Number guessing")
        self.setGeometry(100, 100, 800, 600)

        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Stacked widget for different screen
        self.stacked_widget = QStackedWidget()

        # Main menu
        self.main_menu = self.create_main_menu()
        self.stacked_widget.addWidget(self.main_menu)

        # Game widgets
        self.dice_game = DiceGame(self.stats_manager, self.return_to_menu)
        self.number_game = NumberGuessGame(self.stats_manager, self.return_to_menu)

        self.stacked_widget.addWidget(self.dice_game)
        self.stacked_widget.addWidget(self.number_game)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.stacked_widget)
        central_widget.setLayout(layout)

        # Show main menu initially
        self.stacked_widget.setCurrentWidget(self.main_menu)

    def create_main_menu(self):
        menu_widget = QWidget()
        layout = QVBoxLayout()

        # Title
        title = QLabel("Game Hub")
        title.setFont(QFont("Arial", 24, QFont.bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Game buttons
        dice_btn = QPushButton("Dice Roller Game")
        dice_btn.setFont(QFont("Arial", 14))
        dice_btn.clicked.connect(self.show_dice_game)

        number_btn = QPushButton("Number Guessing Game")
        number_btn.setFont(QFont("Arial", 14))
        number_btn.clicked.connect(self.show_number_game)

        stats_btn = QPushButton("View Statistics")
        stats_btn.setFont(QFont("Arial", 14))
        stats_btn.clicked.connect(self.show_stats)

        quit_btn = QPushButton("Quit")
        quit_btn.setFont(QFont("Arial", 14))
        quit_btn.clicked.connect(self.close)

        # Buttons to layout adding
        layout.addWidget(dice_btn)
        layout.addWidget(number_btn)
        layout.addWidget(stats_btn)
        layout.addWidget(quit_btn)

        layout.setSpacing(20)
        layout.setContentsMargins(50, 50, 50, 50)

        menu_widget.setLayout(layout)
        return menu_widget
    
    def show_dice_game(self):
        self.stacked_widget.setCurrentWidget(self.dice_game)

    def show_number_game(self):
        self.stacked_widget.setCurrentWidget(self.number_game)

    def show_stats(self):
        stats = self.stats_manager.get_all_stats()
        stats_text = "--- Game Statistics ---\n\n"

        # Dice game statistics
        dice_stats = stats.get('dice_game', {})
        stats_text += "DICE ROLLER:\n"
        stats_text += f"Total rolls: {dice_stats.get('total_rolls', 0)}\n"
        stats_text += f"Games played: {dice_stats.get('games_played', 0)}\n"

        if dice_stats.get('roll_counts'):
            stats_text += "Roll distribution:\n"
            for face, count in sorted(dice_stats['roll_counts'].items()):
                stats_text += f"    {face}: {count} times\n"

        stats_text += "\n"

        # Number guessing game statistics
        number_stats = stats.get('number_guesses', {})
        stats_text += "Number Guessing:\n"
        stats_text += f"Games played: {number_stats.get('games_played', 0)}\n"
        stats_text += f"Games won: {number_stats.get('games_won', 0)}\n"
        stats_text += f"Total guesses: {number_stats.get('total_guesses', 0)}\n"

        if number_stats.get('games_played', 0) > 0:
            win_rate = (number_stats.get('games_won', 0) / number_stats['games_played']) * 100
            stats_text += f"Win rate: {win_rate:.1f}%\n"

        if number_stats.get('total_guesses', 0) > 0 and number_stats.get('games_won', 0) > 0:
            avg_guesses = number_stats['total_guesses'] / number_stats['games_won']
            stats_text += f"Average guesses per win: {avg_guesses:.1f}\n"

        # Show stats in a dialog box
        from PyQt5.QtWidgets import QMessageBox
        msg = QMessageBox()
        msg.setWindowTitle("Game Statistics")
        msg.setText(stats_text)
        msg.setFont(QFont("Courier", 10))
        msg.exec_()

    def return_to_menu(self):
        self.stacked_widget.setCurrentWidget(self.main_menu)

    def closeEvent(self, event):
        # Save stats when closing app
        self.stats_manager.save_stats()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())