from tkinter.filedialog import askopenfilename
from pathlib import Path
import os

class Paths:
    def __init__(self):
        # Readonly
        self.root: Path = Path(__file__).resolve().parents[3]
        self.assets: Path = self.root / "assets"
        self.themes: Path = self.assets / "themes"
        self.labels: Path = self.assets / "labels"
        self.settings: Path = self.assets / "settings"
        self.packages: Path = self.settings / "_packages"
        self.pcaptures: Path = self.assets / "pcaptures"
        self.mcaptures: Path = self.assets / "mcaptures"
        self.pages: Path = self.assets / "pages"

        # Dynamically generated, read & write
        self.user_data: Path = self.generate_path(self.root / "user_data")
        self.user_mcaptures: Path = self.generate_path(self.user_data / "mcaptures")
        self.user_pcaptures: Path = self.generate_path(self.user_data / "pcaptures")
        self.user_pages: Path = self.generate_path(self.user_data / "page_data")

    #     self.page_folder_names: list[str] = [f.name for f in self.pages.iterdir() if f.is_dir()]
    #     self.page_folders: list[Path] = [self.pages / folder_name for folder_name in self.page_folder_names]
    #     self.user_page_folders: list[Path] = [self.user_pages / folder_name for folder_name in self.page_folder_names]

    # def get_page_


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

    def generate_path(self, file_path: Path):
        try:
            file_path.mkdir(parents=True, exist_ok=True)
            self.lower_permissions(file_path)
        except Exception as e:
            print(f"Err: [{e}] while generating a directory.")
        finally:
            return file_path

    def lower_permissions(self, path: Path):
        '''
        The app is typically launched with sudo for raw-socket network
        access, so any file or directory it creates comes out owned by
        root - off-limits to the user who actually ran it once the app
        closes. sudo hands the original user's ids down as the
        SUDO_UID/SUDO_GID env vars, so chown the given path back to
        them whenever they're set. A no-op when not running under sudo
        (nothing to hand back) or if the chown fails for any other
        reason (e.g. path doesn't exist).
        '''
        sudo_uid = os.environ.get("SUDO_UID")
        sudo_gid = os.environ.get("SUDO_GID")
        if sudo_uid is None or sudo_gid is None:
            return
        try:
            os.chown(path, int(sudo_uid), int(sudo_gid))
        except Exception as e:
            print(f"Err: [{e}] while lowering permissions on {path}.")