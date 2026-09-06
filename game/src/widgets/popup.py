from customtkinter import CTkBaseClass, CTkToplevel, CTkFrame, CTkLabel, CTkButton  # quit_dialog only - still unmigrated, dead code (unused anywhere)
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

def quit_dialog(master: CTkBaseClass, context: Context, quit_func):
        style = context.style
        window = CTkToplevel(master)
        window.title("Confirm")
        window.config(padx=style.igap, pady=style.igap)
        message = "Are you sure you want to quit?\nNothing will be saved."

        # Center to app
        width = 500
        height = 300
        root_x = master.winfo_rootx()
        root_y = master.winfo_rooty()
        win_x = root_x + master.winfo_width()/2 - width/2
        win_y = root_y + master.winfo_height()/2 - height/2

        window.geometry(f"{width}x{height}+{int(win_x)}+{int(win_y)}")

        # Add widgets to the window
        frame = CTkFrame(window)
        frame.pack(fill="both", side="top", expand=True, padx=style.gap, pady=style.gap)

        label = CTkLabel(frame, text=message, font=style.get_font(), wraplength=width - 2*style.igap)
        label.pack(pady=style.gap, padx=style.gap)

        buttons_frame = CTkFrame(frame)
        buttons_frame.pack(side="bottom")

        quit_button = CTkButton(buttons_frame, text="Yes, quit", command=quit_func, font=style.get_font())
        quit_button.grid(pady=style.gap, column=0, sticky="ew")

        continue_button = CTkButton(buttons_frame, text="No, continue", command=window.destroy, font=style.get_font())
        continue_button.grid(pady=style.gap, column=0, sticky="ew")

        window.transient(master)
        window.update_idletasks()
        window.grab_set()      # block interactions with main window
        window.focus_force()   # force focus to the window
        return window