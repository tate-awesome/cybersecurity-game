from customtkinter import *
from ...app_core.context import Context

class TitleMenu(CTkFrame):
    '''
    The main Widget for the title menu.
    Comes with a title and has a button maker.
    '''

    def __init__(self, master: CTkFrame, context: Context, title_text: str = "Title Menu"):
        self.context = context
        self.style = context.style

        super().__init__(master, fg_color="transparent")
        self.pack(expand="True", fill="both")
        
        self.current_row = 1

        title_label = CTkLabel(self, text=title_text, font= self.style.get_font("title"))
        title_label.grid(row=self.current_row, column=1, pady=self.style.gap2, sticky="sew")
        self.current_row = self.current_row + 1

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=0)
        self.columnconfigure(2, weight=1)

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=0)
        self.rowconfigure(2, weight=1)

    
    def button(self, text: str, function = None):
        button = CTkButton(self, text=text, command=function, font=self.style.get_font("title_btn"))
        button.grid(row = self.current_row, column=1, pady=self.style.gap, ipady=self.style.igap)
        self.rowconfigure(self.current_row, weight=0)
        self.current_row = self.current_row + 1
        self.rowconfigure(self.current_row, weight=1)