import customtkinter as ctk

from .router import Router

import platform


class App():
    '''
    Creates the Router and starts the CTk main loop
    '''

    def __init__(self, start_page="main_menu", title="Game", start_fullscreen = False):

        # Start a CTk app
        self.root = ctk.CTk()
        self.root.title(title)
        self.set_geometry(start_fullscreen)
        
        # Create the router, which will handle page navigation
        Router(self.root, start_page)

        # Start the main loop
        self.root.mainloop()


    def set_geometry(self, start_fullscreen):
        '''
        Sets the size and position of the window, then starts maximized or fullscreen
        '''
        f = 3.0/4.0
        w = int(f*self.root.winfo_screenwidth())
        h = int(f*self.root.winfo_screenheight())
        self.root.geometry(f"{w}x{h}")

        if start_fullscreen:
            self.root.attributes("-fullscreen", True)
        else:
            self.root.after(
                50,
                self.maximize
            )

    
    def maximize(self):
        try:
            self.root.state("zoomed")
        except Exception:
            try:
                self.root.attributes("-zoomed", True)
            except Exception:
                pass