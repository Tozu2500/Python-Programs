"""
Configuration module for the app
Handles themes, settings and also constant values
"""

class Config:

    def __init__(self):
        self.current_theme = "dark"
        self.themes = {
            "dark": {
                "bg_primary": "#2b2b2bff",
                "bg_secondary": "#3c3c3c",
                "bg_accent": "#404040",
                "text_primary": "#ffffff",
                "text_secondary": "#cccccc",
                "text_accent": "#00ff88",
                "button_bg": "#4a4a4a",
                "button_hover": "#5a5a5a",
                "button_pressed": "#3a3a3a",
                "border": "#555555",
                "success": "#00ff88",
                "warning": "#ffaa00",
                "error": "#ff4444"
            },
            "light": {
                "bg_primary": "#ffffff",
                "bg_secondary": "#f5f5f5",
                "bg_accent": "#e0e0e0",
                "text_primary": "#333333",
                "text_secondary": "#666666",
                "text_accent": "#007acc",
                "button_bg": "#e0e0e0",
                "button_hover": "#d0d0d0",
                "button_pressed": "#c0c0c0",
                "border": "#cccccc",
                "success": "#28a745",
                "warning": "#ffc107",
                "error": "dc3545"
            }
        }

        # Time frame multipliers in seconds
        self.time_multipliers = {
            "hour": 3600, # Seconds
            "day": 86400,
            "week": 604800,
            "month": 2628000,
            "year": 31536000
        }

        # Intervals for the frame update
        self.update_interval = 50

    def get_theme(self, theme_name=None):
        theme = theme_name or self.current_theme
        return self.themes.get(theme, self.themes["dark"])
    
    def toggle_theme(self):
        self.current_theme = "light" if self.current_theme == "dark" else "dark"
        return self.current_theme
    
    def get_stylesheet(self, theme_name=None):
        theme = self.get_theme(theme_name)

        return f"""
        QMainWindow {{
            background-color: {theme['bg_primary']};
            color: {theme['text_primary']};
        }}

        QWidget {{
            background-color: {theme['bg_primary']};
            color: {theme['text_primary']};
        }}

        QFrame {{
            border: 1px solid {theme['border']};
            border-radius: 8px;
            background-color: {theme['bg_secondary']};
            padding: 10px;
        }}

        QLabel {{
            background-color: transparent;
            color: {theme['text_primary']};
        }}

        QLabel#title {{
            font-size: 24px;
            font-weight: bold;
            color: {theme['text_accent']};
            background-color: transparent;
        }}

        QLabel#counter {{
            font-size: 36px;
            font-weight: bold;
            color: {theme['success']};
            background-color: transparent;
            border: 2px solid {theme['success']};
            border-radius: 12px;
            padding: 20px;
        }}

        QLabel#info {{
            font-size: 14px;
            color: {theme['text_secondary']};
            background-color: transparent;
        }}

        QPushButton {{
            background-color: {theme['button_bg']};
            border: 1px solid {theme['border']};
            border-radius: 6px;
            padding: 8px 16px;
            font-size: 12px;
            font-weight: bold;
            color: {theme['text_primary']};
        }}

        QPushButton:hover {{
            background-color: {theme['button_hover']};
        }}

        QPushButton:pressed {{
            background-color: {theme['button_pressed']};
        }}

        QPushButton#primary {{
            background-color: {theme['text_accent']};
            color: white;
        }}

        QPushButton#primary:hover {{
            background-color: {theme['success']};
        }}

        QPushButton#danger {{
            background-color: {theme['error']};
            color: white;
        }}

        QPushButton#danger:hover {{
            background-color #ff6666;
        }}

        QLineEdit {{
            background-color: {theme['bg_accent']};
            border: 2px solid {theme['border']};
            border-radius: 6px;
            padding: 8px;
            font-size: 12px;
            color: {theme['text_primary']};
        }}

        QLineEdit:focus {{
            border-color: {theme['text_accent']};
        }}

        QComboBox {{
            background-color: {theme['bg_accent']};
            border: 2px solid {theme['border']};
            border-radius: 6px;
            padding: 8px;
            font-size: 12px;
            color: {theme['text_primary']};
        }}

        QComboBox:focus {{
            border-color: {theme['text_accent']};
        }}

        QComboBox::drop-down {{
            border: none;
            width: 20px;
        }}

        QComboBox::down-arrow {{
            image: none;
            border-left: 5px solid transparent;
            border-right: 5px solid transparent;
            border-top: 5px solid {theme['text_primary']};
            margin-right: 5px;
        }}

        QComboBox QAbstractItemView {{
            background-color: {theme['bg_accent']};
            border: 1px solid {theme['border']};
            selection-background-color: {theme['text_accent']};
            color: {theme['text_primary']};
        }}
        """