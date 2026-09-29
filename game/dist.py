import platform, shutil, subprocess, sys, sysconfig
from pathlib import Path

'''
BUILDS A PORTABLE RELEASE INTO game/dist

    python dist.py

Produces dist/CyberGame_<platform> (see build_name) with assets/
copied next to it. user_data/ is left out - the game creates it on
first run. PyInstaller can't cross-compile, so run this on each OS
you want a build for, from the venv that has PyInstaller installed.
'''

GAME_DIR = Path(__file__).resolve().parent
DIST_DIR = GAME_DIR / "dist"
NAME = "CyberGame"


def build_name() -> str:
    '''
    A PyInstaller build runs on the OS it was built on or newer, and only
    on the same CPU architecture. What "newer" is measured against
    differs per OS, so the name carries whatever actually limits where
    the build can run:
        Linux:   the glibc version (the distro itself doesn't matter)
        macOS:   the minimum macOS version this Python was built for
        Windows: nothing - builds run on any supported Windows version
    e.g. CyberGame_linux_glibc2.41_x86_64, CyberGame_windows_x86_64
    '''
    arch = platform.machine().lower()
    arch = {"amd64": "x86_64", "x64": "x86_64", "aarch64": "arm64"}.get(arch, arch)

    os_name = platform.system()
    if os_name == "Linux":
        libc, version = platform.libc_ver()
        tag = f"linux_{libc}{version}" if libc else "linux"
    elif os_name == "Darwin":
        target = sysconfig.get_config_var("MACOSX_DEPLOYMENT_TARGET") or platform.mac_ver()[0]
        tag = f"macos{target}"
    elif os_name == "Windows":
        tag = "windows"
    else:
        tag = os_name.lower()

    return f"{NAME}_{tag}_{arch}"


def main():
    name = build_name()

    # Start from an empty dist/ so no stale builds or assets linger
    if DIST_DIR.exists():
        print(f"Clearing {DIST_DIR}")
        shutil.rmtree(DIST_DIR)

    # sys.executable -m PyInstaller uses this venv's PyInstaller even if
    # the `pyinstaller` command isn't on PATH
    print("Running PyInstaller...")
    result = subprocess.run(
        [
            sys.executable, "-m", "PyInstaller",
            "--onefile",
            "--name", name,
            "--noconfirm",
            "--clean",
            "--specpath", "build",  # keep the generated .spec out of game/
            "main.py",
        ],
        cwd=GAME_DIR,
    )
    if result.returncode != 0:
        sys.exit(f"PyInstaller failed with exit code {result.returncode}.")

    print("Copying assets...")
    shutil.copytree(GAME_DIR / "assets", DIST_DIR / "assets")

    print(f"Done. Built {name} in {DIST_DIR}")


if __name__ == "__main__":
    main()
