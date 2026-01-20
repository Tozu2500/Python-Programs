import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt5.QtCore import Qt # QT Import for alignment

app = QApplication(sys.argv)

# Main window
window = QWidget()
window.setWindowTitle("Layouts test")
window.setGeometry(100, 100, 500, 500)

# Widgets
label = QLabel("Testing PyQt5")
label.setAlignment(Qt.AlignCenter)

button = QPushButton("Click this")
label2 = QLabel("Hello!")

# Vertical layout (QVBoxLayout) + add widgets
layout = QVBoxLayout()
layout.addWidget(label)
layout.addWidget(button)
layout.addWidget(label2)

# Set the layout on the main window
window.setLayout(layout)

window.show()
sys.exit(app.exec_())