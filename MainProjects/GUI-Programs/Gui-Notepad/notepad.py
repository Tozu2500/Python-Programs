import sys
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QTextEdit, QVBoxLayout,
                            QWidget, QMenuBar, QAction, QFileDialog, QMessageBox,
                            QHBoxLayout, QLabel, QStatusBar, QFontDialog,
                            QColorDialog, QToolBar)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont, QIcon, QKeySequence, QTextCursor

class Notepad(QMainWindow):
    def __init__(self):
        super().__init__()
        self.current_file = None
        self.is_modified = False
        self.init_ui()

    def init_ui(self):
        # Window properties
        self.setWindowTitle("Simple notepad application with Python")
        self.setGeometry(100, 100, 800, 600)

        # Central widget + layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Text editor creating
        self.text_edit = QTextEdit()
        self.text_edit.setFont(QFont("Consolas", 12))
        self.text_edit.textChanged.connect(self.text_changed)
        layout.addWidget(self.text_edit)

        # Create a menubar
        self.create_menu_bar()

        # Create a toolbar
        self.create_toolbar()

        # Create a statusbar
        self.create_status_bar()

        # Set focus to the text editor
        self.text_edit.setFocus()

    def create_menu_bar(self):
        menubar = self.menuBar()

        # File menu
        file_menu = menubar.addMenu("File")

        new_action = QAction("New", self)
        new_action.setShortcut(QKeySequence.New)
        new_action.triggered.connect(self.new_file)
        file_menu.addAction(new_action)

        open_action = QAction("Open", self)
        open_action.setShortcut(QKeySequence.Open)
        open_action.triggered.connect(self.open_file)
        file_menu.addAction(open_action)

        save_action = QAction("Save", self)
        save_action.setShortcut(QKeySequence.Save)
        save_action.triggered.connect(self.save_file)
        file_menu.addAction(save_action)

        save_as_action = QAction("Save As...", self)
        save_as_action.setShortcut(QKeySequence.SaveAs)
        save_as_action.triggered.connect(self.save_as_file)
        file_menu.addAction(save_as_action)

        file_menu.addSeparator()

        exit_action = QAction("Exit", self)
        exit_action.setShortcut(QKeySequence.Quit)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # Editing menu
        edit_menu = menubar.addMenu("Edit")

        undo_action = QAction("Undo", self)
        undo_action.setShortcut(QKeySequence.Undo)
        undo_action.triggered.connect(self.text_edit.undo)
        edit_menu.addAction(undo_action)

        redo_action = QAction("Redo", self)
        redo_action.setShortcut(QKeySequence.Redo)
        redo_action.triggered.connect(self.text_edit.redo)
        edit_menu.addAction(redo_action)

        edit_menu.addSeparator()

        cut_action = QAction("Cut", self)
        cut_action.setShortcut(QKeySequence.Cut)
        cut_action.triggered.connect(self.text_edit.cut)
        edit_menu.addAction(cut_action)

        copy_action = QAction("Copy", self)
        copy_action.setShortcut(QKeySequence.Copy)
        copy_action.triggered.connect(self.text_edit.copy)
        edit_menu.addAction(copy_action)

        paste_action = QAction("Paste", self)
        paste_action.setShortcut(QKeySequence.Paste)
        paste_action.triggered.connect(self.text_edit.paste)
        edit_menu.addAction(paste_action)

        edit_menu.addSeparator()

        select_all_action = QAction("Select all", self)
        select_all_action.setShortcut(QKeySequence.SelectAll)
        select_all_action.triggered.connect(self.text_edit.selectAll)
        edit_menu.addAction(select_all_action)

        # Formatting menu
        format_menu = menubar.addMenu("Format")

        font_action = QAction("Font...", self)
        font_action.triggered.connect(self.change_font)
        format_menu.addAction(font_action)

        color_action = QAction("Text Color...", self)
        color_action.triggered.connect(self.change_color)
        format_menu.addAction(color_action)

        # Help menu
        help_menu = menubar.addMenu("Help")

        about_action = QAction("About", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

    def create_toolbar(self):
        toolbar = QToolBar()
        self.addToolBar(toolbar)

        # Add common actions to toolbar
        new_action = QAction("New", self)
        new_action.triggered.connect(self.new_file)
        toolbar.addAction(new_action)

        open_action = QAction("Open", self)
        open_action.triggered.connect(self.open_file)
        toolbar.addAction(open_action)

        save_action = QAction("Save", self)
        save_action.triggered.connect(self.save_file)
        toolbar.addAction(save_action)

        toolbar.addSeparator()

        undo_action = QAction("Undo", self)
        undo_action.triggered.connect(self.text_edit.undo)
        toolbar.addAction(undo_action)

        redo_action = QAction("Redo", self)
        redo_action.triggered.connect(self.text_edit.redo)
        toolbar.addAction(redo_action)

    def create_status_bar(self):
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        # Add labels for line and column info
        self.position_label = QLabel("Line: 1, Column: 1")
        self.status_bar.addPermanentWidget(self.position_label)

        # Update position when moving
        self.text_edit.cursorPositionChanged.connect(self.update_position)

        self.status_bar.showMessage("Ready")

    def update_position(self):
        cursor = self.text_edit.textCursor()
        line = cursor.blockNumber() + 1
        column = cursor.columnNumber() + 1
        self.position_label.setText(f"Line: {line}, Column: {column}")

    def text_changed(self):
        self.is_modified = True
        self.update_title()

    def update_title(self):
        title = "Simple notepad in Python"
        if self.current_file:
            title += f" - {os.path.basename(self.current_file)}"
        if self.is_modified:
            title += " *"
        self.setWindowTitle(title)

    def new_file(self):
        if self.check_save_changes():
            self.text_edit.clear()
            self.current_file = None
            self.is_modified = False
            self.update_title()
            self.status_bar.showMessage("New file created")

    def open_file(self):
        if self.check_save_changes():
            file_path, _ = QFileDialog.getOpenFileName(
                self,
                "Open File",
                "",
                "Text Files (*.txt);;All Files (*)"
            )
            if file_path:
                try:
                    with open(file_path, 'r', encoding='utf-8') as file:
                        content = file.read()
                        self.text_edit.setPlainText(content)
                        self.current_file = file_path
                        self.is_modified = False
                        self.update_title()
                        self.status_bar.showMessage(f"Opened: {os.path.basename(file_path)}")
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"Couldn't open the file:\n{str(e)}")
                
    def save_file(self):
        if self.current_file:
            self.save_to_file(self.current_file)
        else:
            self.save_as_file()


    def save_as_file(self):
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save File",
            "",
            "Text Files (*.txt);;All Files (*)"
        )
        if file_path:
            self.save_to_file(file_path)

    def save_to_file(self, file_path):
        try:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(self.text_edit.toPlainText())
                self.current_file = file_path
                self.is_modified = False
                self.update_title()
                self.status_bar.showMessage(f"Saved: {os.path.basename(file_path)}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Couldn't save the file:\n{str(e)}")

    def check_save_changes(self):
        if self.is_modified:
            reply = QMessageBox.question(
                self,
                "Save Changes",
                "The document has been modified.\nDo you want to save the changes?",
                QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel
            )
            if reply == QMessageBox.Save:
                self.save_file()
                return not self.is_modified
            elif reply == QMessageBox.Cancel:
                return False
        return True
    
    def change_font(self):
        current_font = self.text_edit.font()
        font, ok = QFontDialog.getFont(current_font, self)
        if ok:
            self.text_edit.setFont(font)

    def change_color(self):
        color = QColorDialog.getColor(Qt.black, self)
        if color.isValid():
            self.text_edit.setStyleSheet(f"color: {color.name()}")

    def show_about(self):
        QMessageBox.about(
            self,
            "About this program",
            "A simple notepad built with Python\n\n"
            "Text editor built with PyQt5.\n"
            "Features:\n"
            "File operations: (New file, Open file, Save file)\n"
            "Editing operations: (Cut, Copy, Paste, Undo and Redo)\n"
            "Font and color customization\n"
            "Status bar with position"
        )

    def closeEvent(self, event):
        if self.check_save_changes():
            event.accept()
        else:
            event.ignore()

def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Simple notepad with python")

    notepad = Notepad()
    notepad.show()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
