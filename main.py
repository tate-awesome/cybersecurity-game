import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
import navigate


root = ctk.CTk()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

root.geometry(f"{int(screen_width*3/4)}x{int(screen_height*3/4)}")
# app.attributes("-fullscreen", True)
# app.state("zoomed")
root.title("Cybersecurity Game")

nav = navigate.Navigate(root)
nav.main_menu()
# nav.hacker_start()


root.mainloop()