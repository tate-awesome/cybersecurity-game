import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
import navigate

# Run as sudo for socket permissions?
# sudo python3 "/home/u-smart/Documents/tate-github/cybersecurity-game/Tate Files/GUI Game/main.py"
# Password = veronica
# Be on GL-SFT1200-ab1 wifi
# Reset device before clicking start buttons
# ctrl+c in terminal to stop os commands
# trash terminal

root = ctk.CTk()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

root.geometry(f"{int(screen_width*3/4)}x{int(screen_height*3/4)}")
# app.attributes("-fullscreen", True)
# app.state("zoomed")
root.title("Cybersecurity Game")

# nav = navigate.Navigate(root)
nav = navigate.Navigate(root)
nav.hacker_hardware_demo()
# nav.hacker_start()


root.mainloop()