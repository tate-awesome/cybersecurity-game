from PySide6.QtWidgets import QDialog, QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QWidget
from ..app_core import Context

def message(master: QWidget, context: Context, message: str):
        style = context.style

        window = QDialog(master)
        window.setWindowTitle("Help")
        window.resize(500, 300)
        window.setModal(True)  # block interactions with main window

        layout = QVBoxLayout(window)

        label = QLabel(message)
        label.setFont(style.get_font())
        label.setWordWrap(True)
        layout.addWidget(label)

        layout.addStretch()

        close_button = QPushButton("Dismiss")
        close_button.setFont(style.get_font())
        close_button.clicked.connect(window.accept)
        layout.addWidget(close_button)

        window.show()
        return window

def confirm_dialog(master: QWidget, context: Context, message: str, confirm_text: str, cancel_text: str, confirm_func):
        '''
        A modal yes/no dialog: shows message, and calls confirm_func only if
        the user presses the confirm_text button.
        '''
        style = context.style

        window = QDialog(master)
        window.setWindowTitle("Confirm")
        window.resize(500, 300)
        window.setModal(True)  # block interactions with main window

        layout = QVBoxLayout(window)

        label = QLabel(message)
        label.setFont(style.get_font())
        label.setWordWrap(True)
        layout.addWidget(label)

        buttons_row = QHBoxLayout()
        layout.addStretch()
        layout.addLayout(buttons_row)

        def confirm():
            confirm_func()
            window.accept()

        confirm_button = QPushButton(confirm_text)
        confirm_button.setFont(style.get_font())
        confirm_button.clicked.connect(confirm)
        buttons_row.addWidget(confirm_button)

        cancel_button = QPushButton(cancel_text)
        cancel_button.setFont(style.get_font())
        cancel_button.clicked.connect(window.reject)
        buttons_row.addWidget(cancel_button)

        window.show()
        return window

def quit_dialog(master: QWidget, context: Context, quit_func):
        message = "Are you sure you want to quit?\nNothing will be saved."
        return confirm_dialog(master, context, message, "Yes, quit", "No, continue", quit_func)
