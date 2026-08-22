from ...app_core import Context
from customtkinter import *
from ..popup import message
from .overlay import Overlay
from CTkToolTip import CTkToolTip

class MenuBar(CTkFrame):
    '''
    The main Widget for the menu bar.
    Comes with a label and has a button maker.
    Inherits CTkFrame.
    '''

    def __init__(self, master: CTkFrame, context: Context, title_label: str = "_default"):
        self.context = context
        self.style = context.style

        super().__init__(master, fg_color=self.style.color("widget"))
        self.pack(side="top", padx=self.style.gap, pady=self.style.gaptop, fill="x")

        self.game_label = CTkLabel(self, text=self.context.labels.get("menu_bar_titles", title_label), font=self.style.get_font(), padx=self.style.igap)
        self.game_label.pack(fill="y", side="left", padx=self.style.gap)

        self.the_overflow_button = None
        self.fine_buttons = []
        self.squashed_buttons = []

        self.overflow_button()

    def add_tooltip(self, widget, key: str):
        self.context.style.add_tooltip(widget, "menu_bar_tooltips", key)

    def add_button(self, label: str="_default", function=None):
        button = CTkButton(self, text=self.context.labels.get("menu_bar_buttons", label), command=function, font=self.style.get_font())
        button.pack(side="right", padx=self.style.gap, pady=self.style.gap)
        return button

    # Button overflow overlay

    def update_squashing(self):
        # Calculate the required width (not including the overflow button)
        required_width = 0
        for child in self.winfo_children():
            if self.the_overflow_button is not None and child == self.the_overflow_button:
                continue
            required_width += child.winfo_reqwidth() + self.style.igap*2

        # Calculate which buttons are squashed or not
        self.fine_buttons = []
        self.squashed_buttons = []
        available_width = self.winfo_width()
        for child in self.winfo_children():
            if child == self.the_overflow_button:
                continue
            available_width -= child.winfo_reqwidth() + self.style.igap*2
            if child == self.game_label:
                continue
            if available_width < 0:
                self.squashed_buttons.append(child)
            else:
                self.fine_buttons.append(child)

    def overflow_button(self):
        text = "..."
        button = CTkButton(self, text=text, command=None, font=self.style.get_font(), width=0)
        self.the_overflow_button = button
        # button.pack(side="right", padx=self.style.gap, pady=self.style.gap, after=self.game_label)
        self.overflow_overlay = Overlay(self.context.root, self.context, button, self.populate_overflow_overlay)

        button.pack_forget()

        def configure_handler(event=None):
            # If the requested width is calculated too early, for example, before a button is done rendering,
            # it will be about 1 button's width too small. So when it's updated in self.add_button, it does update_idletasks()
            try:
                self.update_squashing()
                for squashed in self.squashed_buttons:
                    squashed.pack_forget()
                for fine in self.fine_buttons:
                    fine.pack(side="right", padx=self.style.gap, pady=self.style.gap)
                if len(self.squashed_buttons) > 0:
                    button.pack(side="right", padx=self.style.gap, pady=self.style.gap, after=self.game_label)
                else:
                    button.pack_forget()
            except Exception:
                # A destroyed widget mid-navigation with this <Configure> callback
                # still queued raises TclError from winfo_*/pack/pack_forget -
                # safe to just skip this stale redraw.
                pass

        self.bind("<Configure>", configure_handler)
    
    def clone_button(self, original_button: CTkButton, frame: CTkFrame):
        proxy_button = CTkButton(frame, text=original_button._text, command=original_button._command, font=self.style.get_font())
        proxy_button.pack(side="bottom", padx=self.style.gap, pady=self.style.gap)

        original_button.proxy = proxy_button

    def populate_overflow_overlay(self, overlay):
        for squashed in self.squashed_buttons:
            self.clone_button(squashed, overlay)
            # if (child.winfo_width() < child.winfo_reqwidth() or self.the_overflow_button.) and isinstance(child, CTkButton):
        

    # Panel Buttons


    def minimize_button(self, frame_widget = None, pane = None):
        minimize_text = self.context.labels.get("menu_bar_buttons", "minimize")
        maximize_text = self.context.labels.get("menu_bar_buttons", "maximize")
        button = self.add_button("minimize")
        body_packed = True
        configure_options = {}
        manager = "none"

        if frame_widget is not None:
            manager = frame_widget.winfo_manager()

        def hide_body():
            nonlocal configure_options, body_packed
            if not body_packed:
                return
            if manager == "pack":
                configure_options = frame_widget.pack_info()
                frame_widget.pack_forget()
                body_packed = False
            elif manager == "grid":
                configure_options = frame_widget.grid_info()
                frame_widget.grid_forget()
                body_packed = False
            elif manager == "place":
                configure_options = frame_widget.place_info()
                frame_widget.place_forget()
                body_packed = False
        
        def show_body():
            nonlocal configure_options, body_packed
            if body_packed:
                return
            if manager == "pack":
                frame_widget.pack(**configure_options)
                body_packed = True
            elif manager == "grid":
                frame_widget.grid(**configure_options)
                body_packed = True
            elif manager == "place":
                frame_widget.place(**configure_options)
                body_packed = True

        def shrink_pane():
            if pane is not None:
                pane.master.add(pane, height=self.style.PANE_MIN_HEIGHT)

        def grow_pane():
            if pane is not None:
                if pane.default_size:
                    size = pane.default_size
                else:
                    size = self.style.PANE_BIG
                pane.master.add(pane, height=size*self.style.get_scale_correction())

        def click_minimize():
            button.configure(command=click_maximize, text=maximize_text)
            if hasattr(button, "proxy"):
                button.proxy.configure(command=click_maximize, text=maximize_text)
            shrink_pane()
            hide_body()
        
        def click_maximize():
            button.configure(command=click_minimize, text=minimize_text)
            if hasattr(button, "proxy"):
                button.proxy.configure(command=click_minimize, text=minimize_text)
            grow_pane()
            show_body()
        
        def manual_growth():
            button.configure(command=click_minimize, text=minimize_text)
            show_body()
        
        button.configure(command=click_minimize)

        def configure_handler(event=None):
            try:
                if pane is not None:
                    if pane.winfo_height() < self.style.PANE_MIN_HEIGHT + self.style.igap:
                        click_minimize()
                    else:
                        manual_growth()
            except Exception:
                # See overflow_button's configure_handler - a destroyed pane
                # mid-navigation with this callback still queued raises TclError.
                pass
        if pane is not None:
            pane.bind("<Configure>", configure_handler)

    def reversible_button(self, start_func: callable, stop_func: callable, inactive_label: str, active_label: str, start_active: bool = False):
        inactive_name = self.context.labels.get("menu_bar_buttons", inactive_label)
        active_name = self.context.labels.get("menu_bar_buttons", active_label)
        button = self.add_button(inactive_label)
        def stop():
            stop_func()
            if hasattr(button, "proxy"):
                button.proxy.configure(command=start, text=inactive_name)
            button.configure(command=start, text=inactive_name)

        def start():
            start_func()
            if hasattr(button, "proxy"):
                button.proxy.configure(command=stop, text=active_name)
            button.configure(command=stop, text=active_name)

        # Sync the button's initial text/command to whatever state start_func/stop_func
        # already represent, without re-invoking either (they're already in that state).
        if start_active:
            button.configure(command=stop, text=active_name)
        else:
            button.configure(command=start, text=inactive_name)
        return button

    # Page Buttons

    def quit_button(self):
        button = self.add_button("quit_button", self.context.router.quit)
        self.add_tooltip(button, "quit_button")
    
    def refresh_button(self):
        button = self.add_button("refresh_button", self.context.router.refresh)
        self.add_tooltip(button, "refresh_button")

    def reset_button(self):
        button = self.add_button("reset_button", self.context.reset_data)
        self.add_tooltip(button, "reset_button")

    def back_button(self):
        button = self.add_button("back_button", self.context.router.go_back)
        self.add_tooltip(button, "back_button")
    
    def toggle_button(self):
        button = self.add_button("toggle_button", self.context.style.toggle_mode)
        self.add_tooltip(button, "toggle_button")
    
    def theme_button(self):
        button = self.add_button("theme_button", self.context.style.select_theme)
        self.add_tooltip(button, "theme_button")

    def pcap_button(self):
        button = self.add_button("pcap_button", self.context.net.loader.load_pcap)
        self.add_tooltip(button, "pcap_button")

    def save_button(self):
        button = self.add_button("save_button", self.context.net.replay.save_json)

    def load_button(self):
        button = self.add_button("load_button", self.context.net.replay.load_json)
    
    def preset_button(self):
        button = self.add_button("preset_button", self.context.states.select)
        self.add_tooltip(button, "preset_button")
    
    def labels_button(self):
        button = self.add_button("labels_button", self.context.labels.select)
        self.add_tooltip(button, "labels_button")
    
    def help_button(self):
        button = self.add_button("help_button", lambda: message(self, self.context, self.context.help_message()))
        self.add_tooltip(button, "help_button")

    def data_button(self):
        button = self.add_button("fields_button", self.context.preferences.save_settings)
        self.add_tooltip(button, "fields_button")

    def preferences_button(self):
        button = self.add_button("preferences_button", self.context.preferences.save_preferences)
        self.add_tooltip(button, "preferences_button")

    def page_button(self):
        button = self.add_button("page_button", self.context.preferences.save_page)
        self.add_tooltip(button, "page_button")

    def page_buttons(self):
        self.quit_button()
        self.refresh_button()
        self.reset_button()
        self.back_button()
        self.help_button()
        self.toggle_button()
        self.theme_button()
        self.pcap_button()
        self.save_button()
        self.load_button()
        self.preset_button()
        self.labels_button()
        self.data_button()
        self.preferences_button()
        self.page_button()
        