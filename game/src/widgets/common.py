from customtkinter import *
import tkinter as tk
from . import popup
from ..app_core.context import Context
# from tkinter import ttk

def configure_reversible_button(the_button: CTkButton, start_func: callable, stop_func: callable, func_name: str):
    def stop():
        the_button.configure(text=f"Stopping {func_name}...")
        stop_func()
        the_button.configure(command=start, text=f"Start {func_name}")

    def start():
        the_button.configure(text=f"Starting {func_name}...")
        start_func()
        the_button.configure(command=stop, text=f"Stop {func_name}")
    the_button.configure(command=start, text=f"Start {func_name}")