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
        self.pcaptures = self.assets / "pcaptures"
        self.mcaptures = self.assets / "mcaptures"

    def select_path(self, directory: str, prompt: str, filetypes: list[str] = ["json", "*.json"]):
        try:
            file_path = askopenfilename(
                initialdir=directory,
                title=prompt,
                filetypes=(filetypes)
            )
            if file_path == "" or not isinstance(file_path, str):
                return None
            else:
                return file_path
        except:
            return None