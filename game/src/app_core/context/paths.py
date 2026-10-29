from pathlib import Path
import os, sys

from PySide6.QtWidgets import QApplication, QFileDialog, QMainWindow, QWidget


def file_dialog(prompt: str, directory: str | os.PathLike[str], qt_filter: str, save: bool = False) -> str | None:
    '''
    Asks for a file to open (or, with save, to save to) - None if cancelled.

    Qt's own dialog, not the operating system's: the native Windows one is
    a separate window Qt doesn't manage, which could open behind the
    fullscreen game - invisible, but still blocking every click until it
    was closed. This one is a PySide6 window owned by the game's window,
    so it always opens over it and is themed like the rest of the app.
    '''
    ask = QFileDialog.getSaveFileName if save else QFileDialog.getOpenFileName
    file_path, _ = ask(_dialog_parent(), prompt, str(directory), qt_filter,
                       options=QFileDialog.Option.DontUseNativeDialog)
    return file_path if isinstance(file_path, str) and file_path else None


def _dialog_parent() -> QWidget | None:
    '''The game's main window, for a dialog to open over.'''
    active = QApplication.activeWindow()
    if active is not None:
        return active
    return next((w for w in QApplication.topLevelWidgets() if isinstance(w, QMainWindow) and w.isVisible()), None)


class Paths:
    def __init__(self):
        # Readonly
        # A PyInstaller build's __file__ points inside its bundle (a temp
        # dir for --onefile, _internal/ for --onedir), so anchor to the
        # folder holding the executable instead - assets/ and user_data/
        # ship next to it.
        if getattr(sys, "frozen", False):
            self.root: Path = Path(sys.executable).resolve().parent
        else:
            self.root: Path = Path(__file__).resolve().parents[3]
        self.assets: Path = self.root / "assets"
        self.themes: Path = self.assets / "themes"
        self.labels: Path = self.assets / "labels"
        self.settings: Path = self.assets / "settings"
        self.register_presets: Path = self.settings / "register_presets"
        self.packages: Path = self.settings / "_packages"
        self.pcaptures: Path = self.assets / "pcaptures"
        self.mcaptures: Path = self.assets / "mcaptures"
        self.pages: Path = self.assets / "pages"
        # The icon font (see style.ICONS)
        self.fonts: Path = self.assets / "fonts"
        # The window and taskbar icon (see App.set_icon)
        self.icons: Path = self.assets / "icons"

        # Dynamically generated, read & write. _user_dirs is the single
        # source of truth for the user_data tree so DeleteAllUserData's
        # recreate (see important_buttons) stays in sync when a dir is added here.
        self.user_data: Path = self.root / "user_data"
        self.user_mcaptures: Path = self.user_data / "mcaptures"
        self.user_pcaptures: Path = self.user_data / "pcaptures"
        self.user_pages: Path = self.user_data / "page_data"
        # Imported themes - see style.IMPORTED_PREFIX
        self.user_themes: Path = self.user_data / "themes"
        # Files the app makes for itself and can make again (e.g. Style.texture_image)
        self.user_cache: Path = self.user_data / "cache"
        self._user_dirs: tuple[Path, ...] = (self.user_data, self.user_mcaptures, self.user_pcaptures, self.user_pages,
                                             self.user_themes, self.user_cache)
        self.create_user_dirs()

    #     self.page_folder_names: list[str] = [f.name for f in self.pages.iterdir() if f.is_dir()]
    #     self.page_folders: list[Path] = [self.pages / folder_name for folder_name in self.page_folder_names]
    #     self.user_page_folders: list[Path] = [self.user_pages / folder_name for folder_name in self.page_folder_names]

    # def get_page_


    def create_user_dirs(self):
        '''
        (Re)create the user_data directory tree. generate_path is a no-op
        for dirs that already exist, so this is safe both on a fresh start
        and after DeleteAllUserData wipes the tree.
        '''
        for path in self._user_dirs:
            self.generate_path(path)

    def select_path(self, directory: str | os.PathLike[str], prompt: str, filetypes: list[tuple[str, str]] | None = None) -> str | None:
        if filetypes is None:
            filetypes = [("json", "*.json")]
        try:
            return file_dialog(prompt, directory, self._to_qt_filter(filetypes))
        except Exception:
            return None

    @staticmethod
    def _to_qt_filter(filetypes: list[tuple[str, str]]) -> str:
        '''
        Qt's file dialogs take a single ";;"-separated filter string
        (e.g. "PCAP files (*.pcap *.pcapng);;All files (*.*)") instead of
        tkinter's list of (label, pattern) tuples, so callers that still
        pass the tkinter-style filetypes list need it converted.
        '''
        return ";;".join(f"{label} ({patterns})" for label, patterns in filetypes)

    def generate_path(self, file_path: Path):
        try:
            # mkdir(parents=True) can create several directories at once;
            # hand every one of them back, not just the leaf.
            created = [p for p in (file_path, *file_path.parents) if not p.exists()]
            file_path.mkdir(parents=True, exist_ok=True)
            for path in created:
                self.lower_permissions(path)
            self.lower_permissions(file_path)
        except Exception as e:
            print(f"Err: [{e}] while generating a directory.")
        # Return outside finally: a return in finally swallows anything the
        # except doesn't catch (KeyboardInterrupt/SystemExit), hiding Ctrl-C.
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