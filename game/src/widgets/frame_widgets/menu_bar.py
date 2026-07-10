from ...app_core.context import Context
from customtkinter import *
from ..popup import message

class MenuBar(CTkFrame):
    '''
    The main Widget for the menu bar.
    Comes with a label and has a button maker.
    Inherits CTkFrame.
    '''

    def __init__(self, master: CTkFrame, context: Context, title_text: str = "Page"):
        self.context = context
        self.style = context.style

        super().__init__(master, fg_color=self.style.color("widget"))
        self.pack(side="top", padx=self.style.gap, pady=self.style.gaptop, fill="x")

        game_label = CTkLabel(self, text=title_text, font=self.style.get_font(), padx=self.style.igap)
        game_label.pack(fill="y", side="left", padx=self.style.gap)

    def add_button(self, text, function=None):
        button = CTkButton(self, text=text, command=function, font=self.style.get_font())
        button.pack(side="right", padx=self.style.gap, pady=self.style.gap)
        return button

    def quit_button(self):
        self.add_button("Quit", self.context.router.quit)
    
    def refresh_button(self):
        self.add_button("Refresh", self.context.router.refresh)

    def back_button(self):
        self.add_button("Back to Title", self.context.router.go_back)
    
    def toggle_button(self):
        self.add_button("Toggle Theme", self.context.router.mode_toggle)
    
    def theme_button(self):
        self.add_button("Select Theme", self.context.router.select_theme)

    def pcap_button(self):
        self.add_button("Load PCAP File", self.context.net.loader.load_pcap)
    
    def preset_button(self):
        self.add_button("Load Preset", self.context.router.select_preset)
    
    def help_button(self):
        self.add_button("Help", lambda: message(self, self.context, self.context.help_message()))

    def minimize_button(self, frame_widget = None, pane = None):
        button = self.add_button("Minimize")
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
                pane.master.add(pane, height=self.style.PANE_MIN)

        def grow_pane():
            if pane is not None:
                pane.master.add(pane, height=self.style.PANE_BIG)

        def click_minimize():
            button.configure(command=click_maximize, text="Maximize")
            shrink_pane()
            hide_body()
        
        def click_maximize():
            button.configure(command=click_minimize, text="Minimize")
            grow_pane()
            show_body()
        
        def manual_growth():
            button.configure(command=click_minimize, text="Minimize")
            show_body()
        
        button.configure(command=click_minimize)

        def configure_handler(event=None):
            if pane is not None:
                if pane.winfo_height() < self.style.PANE_MIN + self.style.igap:
                    click_minimize()
                else:
                    manual_growth()
        if pane is not None:
            pane.bind("<Configure>", configure_handler)


    def reversible_button(self, start_func: callable, stop_func: callable, inactive_name: str, active_name: str):
        button = self.add_button(inactive_name)
        def stop():
            stop_func()
            button.configure(command=start, text=inactive_name)

        def start():
            start_func()
            button.configure(command=stop, text=active_name)
        button.configure(command=start, text=inactive_name)
        return button


    def all_buttons(self):
        self.quit_button()
        self.refresh_button()
        self.back_button()
        self.toggle_button()
        self.theme_button()
        self.pcap_button()
        self.preset_button()
        self.help_button()
        