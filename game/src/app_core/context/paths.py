from tkinter.filedialog import askopenfilename
from pathlib import Path

class Paths:
    def __init__(self):
        self.root = Path(__file__).resolve().parents[3]
        self.assets = self.root / "assets"
        self.themes = self.assets / "themes"
        self.labels = self.assets / "labels"
        self.settings = self.assets / "settings"
        self.packages = self.settings / "_packages"
        self.preferences = self.assets / "preferences"

    def select_path(self, directory: str, prompt: str):
        try:
            file_path = askopenfilename(
                initialdir=directory,
                title=prompt,
                filetypes=(("json", "*.json"),)
            )
            if file_path == "" or not isinstance(file_path, str):
                return None
            else:
                return file_path
        except:
            return None