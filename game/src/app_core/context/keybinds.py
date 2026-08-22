from customtkinter import CTk

from .style import Style

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .. import Context

class KeyBinds:
    '''
    Adds global keybinds and event handlers to the app.
    Includes zoom controls (Ctrl +, Ctrl -, Ctrl 0), fullscreen toggle (F11), and exit fullscreen (Escape).
    Also runs Router.quit() when the window is closed.
    '''

    def __init__(self, context: "Context"):
        '''
        Binds all events
        '''
        self.context = context
        self.root = context.root
        self.style = context.style
        self.refresh = context.router.refresh
        self.quit = context.router.quit

        # Page zoom control
        self.root.bind("<Control-plus>", self.zoom_in)            # Ctrl +
        self.root.bind("<Control-minus>", self.zoom_out)          # Ctrl -
        self.root.bind("<Control-0>", self.zoom_default)          # Ctrl 0
        self.root.bind("<Control-equal>", self.zoom_in)   # (linux) Ctrl = also works as Ctrl +

        # Key events
        # self.style.root.bind("<Key>", self.print_key)

        # Fullscreen control
        self.root.bind("<F11>", self.toggle_fullscreen)
        self.root.bind("<Escape>", self.exit_fullscreen)

        # On close event
        self.root.protocol("WM_DELETE_WINDOW", self.quit)
        # self.root.bind("<FocusOut>", self.minimize_on_tab_if_fullscreen)

        if start_fullscreen := self.context.preferences.get("fullscreen"):
            self.root.after(50,lambda:self.root.attributes("-fullscreen", start_fullscreen))

    def toggle_fullscreen(self, event=None):
        switch_fullscreen = not bool(self.root.attributes("-fullscreen"))
        self.context.preferences.set("fullscreen", str(switch_fullscreen))
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

    
    def print_key(self, e):
        print(e.keysym, e.state)