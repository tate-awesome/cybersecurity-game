from customtkinter import CTk

from .style import Style


class KeyBinds:
    '''
    Adds global keybinds and event handlers to the app.
    Includes zoom controls (Ctrl +, Ctrl -, Ctrl 0), fullscreen toggle (F11), and exit fullscreen (Escape).
    Also runs Router.quit() when the window is closed.
    '''

    def __init__(self, root: CTk, style: Style, refresh: callable, quit: callable):
        '''
        Binds all events
        '''

        self.root = root
        self.style = style
        self.refresh = refresh
        self.quit = quit

        # Page zoom control
        root.bind("<Control-plus>", self.zoom_in)            # Ctrl +
        root.bind("<Control-minus>", self.zoom_out)          # Ctrl -
        root.bind("<Control-0>", self.zoom_default)          # Ctrl 0
        root.bind("<Control-equal>", self.zoom_in)   # (linux) Ctrl = also works as Ctrl +

        # Key events
        # self.style.root.bind("<Key>", self.print_key)

        # Fullscreen control
        root.bind("<F11>", self.toggle_fullscreen)
        root.bind("<Escape>", self.exit_fullscreen)

        # On close event
        root.protocol("WM_DELETE_WINDOW", self.quit)
        # self.root.bind("<FocusOut>", self.minimize_on_tab_if_fullscreen)


    def toggle_fullscreen(self, event=None):
        switch_fullscreen = not bool(self.root.attributes("-fullscreen"))
        self.root.attributes("-fullscreen", switch_fullscreen)

    def minimize_on_tab_if_fullscreen(self, event=None):
        # Ensure the event is for the root window and not an internal widget
        is_fullscreen = bool(self.root.attributes("-fullscreen"))
        if event.widget == self.root and is_fullscreen:
            self.root.iconify()


    def exit_fullscreen(self, event=None):
        self.root.attributes("-fullscreen", False)


    def zoom_in(self, event=None):
        next_index = self.style.ui_scales.index(int(self.style.ui_scale)) + 1
        if next_index >= len(self.style.ui_scales):
            return
        self.style.ui_scale = float(self.style.ui_scales[next_index])
        self.refresh()


    def zoom_out(self, event=None):
        next_index = self.style.ui_scales.index(int(self.style.ui_scale)) - 1
        if next_index < 0:
            return
        self.style.ui_scale = float(self.style.ui_scales[next_index])
        self.refresh()


    def zoom_default(self, event=None):
        self.style.ui_scale = 100.0
        self.refresh()

    
    def print_key(e):
        print(e.keysym, e.state)