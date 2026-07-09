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
        if frame_widget is not None:
            manager = frame_widget.winfo_manager()

            if manager == "pack":
                forget_func = lambda: frame_widget.pack_forget()
                configure_options = frame_widget.pack_info()
                replace_func = lambda: frame_widget.pack(**configure_options)
            elif manager == "grid":
                forget_func = lambda: frame_widget.grid_forget()
                configure_options = frame_widget.grid_info()
                replace_func = lambda: frame_widget.grid(**configure_options)
            elif manager == "place":
                forget_func = lambda: frame_widget.place_forget()
                configure_options = frame_widget.place_info()
                replace_func = lambda: frame_widget.place(**configure_options)
        else:
            forget_func = lambda: ...
            configure_options = {}
            replace_func = lambda: ...

        # if pane is not None:
        #     pane.update_idletasks()
        #     original_height = pane.winfo_height() * self.style.get_scale_correction()
        previous_height = 0

        def minimize():
            forget_func()
            if pane is not None:
                self.update_idletasks()
                previous_height = pane.winfo_height()
                pane.master.add(pane, height=self.winfo_height()+2*self.style.igap)

        def maximize():
            replace_func()
            if pane is not None:
                pane.master.add(pane, height=previous_height)


        self.reversible_button(minimize, maximize, "Minimize", "Maximize")

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
        