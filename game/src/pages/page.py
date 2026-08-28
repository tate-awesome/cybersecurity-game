from customtkinter import CTkFrame
from ..app_core import Context

class Page(CTkFrame):
    '''
    Superclass for pages. Inherits CTkFrame.
    '''

    def __init__(self, context: Context):
        self.context = context
        self.router = context.router
        self.style = context.style
        
        super().__init__(context.root, fg_color=self.style.color("root"))
        self.pack(expand="True", fill="both")

    def load_page(self, file_name: str):
        print("load page")
        path = self.context.paths.pages / file_name
        print(path)
        config = self.context.json.load(path)
        self.parse_config(config)

    def parse_config(self, config: dict):
        # NET for now will be manual
        # this can remove dependency on context
        # menu bar requires title key and ordered list of buttons
        print(config)
        # self.title_label = config.get("title")
        # # settings package and files. Page will use this as the base
        # base_settings = config.get("settings")
        # if base_settings is not None:
        # self.context.paths.pages / path
        # self.context.json.load()
        # self.base_settings = config.get("")
