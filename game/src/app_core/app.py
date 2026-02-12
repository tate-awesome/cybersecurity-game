import customtkinter as ctk
from .router import Router


class App():

    def __init__(self, start_page="main_menu", title="Game", start_fullscreen = False):

        root = ctk.CTk()
        root.title(title)

        if start_fullscreen:
            root.attributes("-fullscreen", True)
        else:
            screen_width = root.winfo_screenwidth()
            screen_height = root.winfo_screenheight()
            root.geometry(f"{int(screen_width*3/4)}x{int(screen_height*3/4)}")

        Router(root, start_page)

        root.mainloop()