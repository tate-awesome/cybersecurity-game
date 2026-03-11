import customtkinter as ctk


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("800x500")

        # Fake menu bar
        self.menu_bar = ctk.CTkFrame(self, height=35)
        self.menu_bar.pack(fill="x")

        self.file_btn = ctk.CTkButton(
            self.menu_bar,
            text="File",
            width=60,
            command=self.file_clicked
        )
        self.file_btn.pack(side="left", padx=5, pady=5)

        self.edit_btn = ctk.CTkButton(
            self.menu_bar,
            text="Edit",
            width=60
        )
        self.edit_btn.pack(side="left", padx=5, pady=5)

        # Main content
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(fill="both", expand=True)

    def file_clicked(self):
        print("Show dropdown here")


app = App()
app.mainloop()