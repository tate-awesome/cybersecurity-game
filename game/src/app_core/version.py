import json
import platform
import subprocess
import threading
from pathlib import Path

# The app's version - bump by hand on a release
VERSION = "0.1.0"

# Written next to assets/ by dist.py, since a PyInstaller build has no
# git checkout to ask
BUILD_FILE = "build.json"


class BuildInfo:
    '''
    Which code is running: VERSION, plus the git commit and branch it was
    built from (and, from source, whether there are uncommitted changes).

    A build reads them from assets/build.json (see dist.py). From source
    they come from git, asked on a background thread so startup doesn't
    wait on it - commit stays None until it answers, or for good if git
    can't (not installed, or refusing a checkout owned by another user
    because the app runs elevated).
    '''

    def __init__(self, assets: Path):
        self.version: str = VERSION
        self.commit: str | None = None
        self.branch: str | None = None
        self.dirty: bool = False
        self.built: str | None = None
        self.from_build = self._load_build_file(assets / BUILD_FILE)
        if not self.from_build:
            threading.Thread(target=self._ask_git, args=(assets.parent,), daemon=True).start()

    def _load_build_file(self, path: Path) -> bool:
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            return False
        if not isinstance(data, dict):
            return False
        self.commit = data.get("commit") if isinstance(data.get("commit"), str) else None
        self.branch = data.get("branch") if isinstance(data.get("branch"), str) else None
        self.built = data.get("built") if isinstance(data.get("built"), str) else None
        return True

    def _ask_git(self, folder: Path):
        commit = git(folder, "rev-parse", "--short", "HEAD")
        if commit is None:
            return
        self.branch = git(folder, "rev-parse", "--abbrev-ref", "HEAD")
        self.dirty = bool(git(folder, "status", "--porcelain", "--untracked-files=no"))
        # Set last - the footer shows the commit once it's there, by then with the rest
        self.commit = commit


def git(folder: Path, *args: str) -> str | None:
    '''A git command's output, stripped - or None if it couldn't run or failed.'''
    # Elevated (sudo/admin), git refuses a checkout another user owns
    # unless told it's safe; only this one command is told so
    command = ["git", "-c", f"safe.directory={folder.as_posix()}", "-C", str(folder), *args]
    flags = subprocess.CREATE_NO_WINDOW if platform.system() == "Windows" else 0
    try:
        result = subprocess.run(command, capture_output=True, text=True, timeout=5, creationflags=flags)
    except (OSError, subprocess.SubprocessError):
        return None
    if result.returncode != 0:
        return None
    return result.stdout.strip()
