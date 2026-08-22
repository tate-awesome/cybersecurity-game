from tkinter.filedialog import askopenfilename
from pathlib import Path
import os

class Paths:
    def __init__(self):
        self.root: Path = Path(__file__).resolve().parents[3]
        self.assets: Path = self.root / "assets"
        self.themes: Path = self.assets / "themes"
        self.labels: Path = self.assets / "labels"
        self.settings: Path = self.assets / "settings"
        self.packages: Path = self.settings / "_packages"
        self.preferences: Path = self.assets / "preferences"
        self.pcaptures: Path = self.assets / "pcaptures"
        self.mcaptures: Path = self.assets / "mcaptures"

    def select_path(self, directory: str | os.PathLike[str], prompt: str, filetypes: list[tuple[str, str]] = [("json", "*.json")]) -> str | None:
        try:
            file_path = askopenfilename(
                initialdir=directory,
                title=prompt,
                filetypes=filetypes
            )
            if file_path == "" or not isinstance(file_path, str):
                return None
            else:
                return file_path
        except Exception:
            return None