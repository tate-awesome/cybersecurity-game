import customtkinter as ctk

class App():

    def __init__(self, title = "Game", start_fullscreen = False):

        self.root = ctk.CTk()
        self.root.title(title)

        # Fullscreen control
        self.is_fullscreen = start_fullscreen
        if self.is_fullscreen:
            self.root.attributes("-fullscreen", True)
        else:
            screen_width = self.root.winfo_screenwidth()
            screen_height = self.root.winfo_screenheight()
            self.root.geometry(f"{int(screen_width*3/4)}x{int(screen_height*3/4)}")
        self.root.bind("<F11>", self.toggle_fullscreen)
        self.root.bind("<Escape>", self.exit_fullscreen)

        # Start 
        self.root.mainloop()

        



    def toggle_fullscreen(self, event=None):
        self.is_fullscreen = not self.is_fullscreen
        self.root.attributes("-fullscreen", self.is_fullscreen)


    def exit_fullscreen(self, event=None):
        self.is_fullscreen = False
        self.root.attributes("-fullscreen", False)



