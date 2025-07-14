import sys
from PyQt5.QtWidgets import QApplication
from gui.main_window import SystemInfoApp

def main():
    app = QApplication(sys.argv)
    window = SystemInfoApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()