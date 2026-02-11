import tkinter as tk
from tkinter import ttk
from . import widgets as ws
import customtkinter as ctk

def run():
        # app_color = "#6F8695"
        water_color = "#003459"



        app = ctk.CTk()
        app.geometry("1000x600")
        # app.attributes("-fullscreen", True)
        # app.state("zoomed")
        app.title("Cybersecurity Game")



        game = ws.Window(ctk, app)
        game.navigate_main_menu()

        # game.create_panes(app)
        # game.create_ip_frame(game.left_pane)
                # self.after(3000, lambda: game.open_popup(self, "Welcome to the game yo"))
                

        # Start the self updating sniffer
                # def network_recon():
                #     ws.sniffer_pane(left_pane, network_recon_btn, middle_pane, 200, right_pane)

                # network_recon_btn.config(command=network_recon)

        app.mainloop()