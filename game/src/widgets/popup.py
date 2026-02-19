from customtkinter import *
from .style import Style

def open(style: Style, master: CTkBaseClass, message: str):
        window = CTkToplevel(master)
        window.title("Help")
        window.config(padx=style.igap, pady=style.igap)

        # Center to app
        width = 500
        height = 300
        root_x = master.winfo_rootx()
        root_y = master.winfo_rooty()
        win_x = root_x + master.winfo_width()/2 - width/2
        win_y = root_y + master.winfo_height()/2 - height/2

        window.geometry(f"{width}x{height}+{int(win_x)}+{int(win_y)}")

        # Geometry

        # Add widgets to the window
        frame = CTkFrame(window)
        frame.pack(fill="both", side="top", expand=True, padx=style.gap, pady=style.gap)

        label = CTkLabel(frame, text=message, font=style.get_font())
        label.pack(pady=style.gap, padx=style.gap)

        close_button = CTkButton(frame, text="Dismiss", command=window.destroy, font=style.get_font())
        close_button.pack(pady=style.gap, side="bottom")

        window.transient(master)
        window.update_idletasks()
        window.grab_set()      # block interactions with main window
        window.focus_force()   # force focus to the window
        return window