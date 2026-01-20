"""
Modern stylesheet for the Salary Counter application.
"""


class StyleSheet:
    """Contains all styling definitions for the application."""
    
    @staticmethod
    def get_stylesheet() -> str:
        """
        Returns the complete stylesheet for the application.
        
        Returns:
            CSS stylesheet as string
        """
        return """
        QMainWindow {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                      stop:0 #667eea, stop:1 #764ba2);
            color: #ffffff;
        }
        
        QWidget {
            background: transparent;
            color: #ffffff;
        }
        
        QLabel#title {
            font-size: 28px;
            font-weight: bold;
            color: #ffffff;
            padding: 20px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 15px;
            margin-bottom: 10px;
        }
        
        QFrame#inputFrame {
            background: rgba(255, 255, 255, 0.15);
            border-radius: 15px;
            padding: 20px;
            margin: 10px 0;
        }
        
        QFrame#counterFrame {
            background: rgba(255, 255, 255, 0.2);
            border-radius: 20px;
            padding: 30px;
            margin: 20px 0;
            border: 2px solid rgba(255, 255, 255, 0.3);
        }
        
        QLabel#inputLabel {
            font-size: 16px;
            font-weight: 600;
            color: #ffffff;
            min-width: 100px;
            margin-right: 10px;
        }
        
        QLineEdit#salaryInput {
            font-size: 16px;
            padding: 12px 15px;
            border: 2px solid rgba(255, 255, 255, 0.3);
            border-radius: 8px;
            background: rgba(255, 255, 255, 0.9);
            color: #333333;
            min-height: 20px;
        }
        
        QLineEdit#salaryInput:focus {
            border: 2px solid #4CAF50;
            background: rgba(255, 255, 255, 1.0);
        }
        
        QLineEdit#salaryInput::placeholder {
            color: #888888;
        }
        
        QComboBox#timeframeCombo {
            font-size: 16px;
            padding: 12px 15px;
            border: 2px solid rgba(255, 255, 255, 0.3);
            border-radius: 8px;
            background: rgba(255, 255, 255, 0.9);
            color: #333333;
            min-height: 20px;
            min-width: 150px;
        }
        
        QComboBox#timeframeCombo:focus {
            border: 2px solid #4CAF50;
            background: rgba(255, 255, 255, 1.0);
        }
        
        QComboBox#timeframeCombo::drop-down {
            subcontrol-origin: padding;
            subcontrol-position: top right;
            width: 30px;
            border-left: 1px solid rgba(255, 255, 255, 0.3);
            background: rgba(255, 255, 255, 0.1);
        }
        
        QComboBox#timeframeCombo::down-arrow {
            image: none;
            border: 1px solid #666666;
            width: 0;
            height: 0;
            border-left: 5px solid transparent;
            border-right: 5px solid transparent;
            border-top: 5px solid #666666;
        }
        
        QComboBox#timeframeCombo QAbstractItemView {
            background: rgba(255, 255, 255, 0.95);
            color: #333333;
            selection-background-color: #4CAF50;
            selection-color: #ffffff;
            border: 1px solid rgba(255, 255, 255, 0.3);
            border-radius: 5px;
        }
        
        QPushButton {
            font-size: 16px;
            font-weight: 600;
            padding: 15px 25px;
            border: none;
            border-radius: 10px;
            margin: 5px;
            min-width: 120px;
        }
        
        QPushButton#startButton {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                      stop:0 #4CAF50, stop:1 #45a049);
            color: #ffffff;
        }
        
        QPushButton#startButton:hover {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                      stop:0 #45a049, stop:1 #3d8b40);
        }
        
        QPushButton#startButton:pressed {
            background: #3d8b40;
        }
        
        QPushButton#startButton:disabled {
            background: #cccccc;
            color: #666666;
        }
        
        QPushButton#stopButton {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                      stop:0 #f44336, stop:1 #d32f2f);
            color: #ffffff;
        }
        
        QPushButton#stopButton:hover {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                      stop:0 #d32f2f, stop:1 #b71c1c);
        }
        
        QPushButton#stopButton:pressed {
            background: #b71c1c;
        }
        
        QPushButton#stopButton:disabled {
            background: #cccccc;
            color: #666666;
        }
        
        QPushButton#resetButton {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                      stop:0 #2196F3, stop:1 #1976D2);
            color: #ffffff;
        }
        
        QPushButton#resetButton:hover {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                      stop:0 #1976D2, stop:1 #1565C0);
        }
        
        QPushButton#resetButton:pressed {
            background: #1565C0;
        }
        
        QLabel#counterTitle {
            font-size: 18px;
            font-weight: 600;
            color: #ffffff;
            margin-bottom: 10px;
        }
        
        QLabel#counterDisplay {
            font-size: 48px;
            font-weight: bold;
            color: #ffffff;
            background: rgba(0, 0, 0, 0.2);
            border-radius: 15px;
            padding: 20px;
            margin: 10px 0;
            border: 2px solid rgba(255, 255, 255, 0.3);
            font-family: 'Courier New', monospace;
        }
        
        QLabel#statusLabel {
            font-size: 14px;
            color: rgba(255, 255, 255, 0.8);
            font-style: italic;
            margin-top: 10px;
        }
        """