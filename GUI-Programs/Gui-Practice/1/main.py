import sys
from PyQt5.QtWidgets import QApplication, QWidget

# Create the application object
app = QApplication(sys.argv)

# Main window
window = QWidget()
window.setWindowTitle("Qt5 practice")
window.setGeometry(100, 100, 400, 300)

window.show()

sys.exit(app.exec_())