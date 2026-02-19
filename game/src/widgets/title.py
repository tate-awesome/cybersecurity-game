from customtkinter import *
from ..widgets.style import Style


def buttons_wrapper(parent):
    wrapper = CTkFrame(parent, fg_color="transparent")
    wrapper.grid(row=2, column=1)
    return wrapper

def button(style: Style, parent, text, function):
    button = CTkButton(parent, text=text, command=function, font=style.get_font("title_btn"))
    button.pack(pady=style.gap, ipady=style.igap)
    return button

def title(parent, text):
    title_font = CTkFont(family="Arial", size=72, weight="bold")
    title_label = CTkLabel(
            parent,
            text=text,
            font=title_font
        )
    title_label.grid(row=1, column=1, ipady=20)

    for i in [0, 3]:
        parent.grid_rowconfigure(i, weight=1)
        parent.grid_columnconfigure(i, weight=1)
    parent.grid_rowconfigure(1, weight=0)
    parent.grid_columnconfigure(1, weight=0)

    return title_label