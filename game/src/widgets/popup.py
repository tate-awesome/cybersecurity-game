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

def delete_user_data_dialog(master: QWidget, context: Context, delete_func):
        style = context.style
        message = "Are you sure you want to delete all user data?\nSaved page progress, captures, and preferences will be permanently lost."

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
            delete_func()
            window.accept()

        delete_button = QPushButton("Yes, delete")
        delete_button.setFont(style.get_font())
        delete_button.clicked.connect(confirm)
        buttons_row.addWidget(delete_button)

        cancel_button = QPushButton("No, cancel")
        cancel_button.setFont(style.get_font())
        cancel_button.clicked.connect(window.reject)
        buttons_row.addWidget(cancel_button)

        window.show()
        return window

def quit_dialog(master: QWidget, context: Context, quit_func):
        style = context.style
        message = "Are you sure you want to quit?\nNothing will be saved."

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
            quit_func()
            window.accept()

        quit_button = QPushButton("Yes, quit")
        quit_button.setFont(style.get_font())
        quit_button.clicked.connect(confirm)
        buttons_row.addWidget(quit_button)

        continue_button = QPushButton("No, continue")
        continue_button.setFont(style.get_font())
        continue_button.clicked.connect(window.reject)
        buttons_row.addWidget(continue_button)

        window.show()
        return window