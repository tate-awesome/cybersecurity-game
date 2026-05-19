import customtkinter as ctk

from .router import Router


class App():
    '''
    Creates the Router and starts the CTk main loop
    '''

    def __init__(self, start_page="main_menu", title="Game", start_fullscreen = False):

        # Start a CTk app
        root = ctk.CTk()
        root.title(title)

        if start_fullscreen:
            root.attributes("-fullscreen", True)
        else:
            # Set the window size to 3/4 of the screen size
            screen_width = root.winfo_screenwidth()
            screen_height = root.winfo_screenheight()
            root.geometry(f"{int(screen_width*3/4)}x{int(screen_height*3/4)}")

        # Create the router, which will handle page navigation
        Router(root, start_page)

        # Start the main loop
        root.mainloop()