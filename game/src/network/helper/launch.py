'''
Launching the privileged helper process (see host.PrivilegedHelper).

The GUI runs as the normal user; this starts a *second* copy of the same
program with the "--helper" flag, elevated, so only that small process runs
with admin/root. A multiprocessing.Process or a plain subprocess can't do
this - a child inherits the parent's privileges - so each platform's own
elevation tool is used instead:

  Windows  ShellExecuteExW with the "runas" verb (one UAC prompt)
  Linux    pkexec if present, else sudo (a graphical/terminal password prompt)
  macOS    osascript "with administrator privileges"

Set CYBERGAME_HELPER_NO_ELEVATE=1 to launch it with the same privileges as
the GUI (no prompt) - for development and for the tests, which can't drive a
real elevation dialog.

spawn() returns a small handle exposing just what the lifecycle needs:
poll() (None while alive, else the exit code) and terminate().
'''
import os
import platform
import shutil
import subprocess
import sys


def spawn(argv: list[str]) -> "HelperHandle":
    if os.environ.get("CYBERGAME_HELPER_NO_ELEVATE") == "1":
        return _PopenHandle(subprocess.Popen(argv))
    system = platform.system()
    if system == "Windows":
        return _spawn_windows(argv)
    if system == "Linux":
        return _spawn_linux(argv)
    if system == "Darwin":
        return _spawn_mac(argv)
    # Unknown platform - best effort, unelevated
    return _PopenHandle(subprocess.Popen(argv))


class HelperHandle:
    def poll(self) -> int | None:
        raise NotImplementedError

    def terminate(self) -> None:
        raise NotImplementedError


class _PopenHandle(HelperHandle):
    def __init__(self, process: subprocess.Popen):
        self._process = process

    def poll(self) -> int | None:
        return self._process.poll()

    def terminate(self) -> None:
        try:
            self._process.terminate()
        except Exception:
            pass


def _spawn_linux(argv: list[str]) -> HelperHandle:
    runner = "pkexec" if shutil.which("pkexec") else ("sudo" if shutil.which("sudo") else None)
    if runner is None:
        raise RuntimeError("neither pkexec nor sudo is available to elevate the helper")
    return _PopenHandle(subprocess.Popen([runner, *argv]))


def _spawn_mac(argv: list[str]) -> HelperHandle:
    # osascript gives the password prompt; the handle is to osascript, which
    # lives as long as the helper it launched (it waits on it).
    quoted = " ".join(f"'{a}'" for a in argv)
    script = f'do shell script "{quoted}" with administrator privileges'
    return _PopenHandle(subprocess.Popen(["osascript", "-e", script]))


def _spawn_windows(argv: list[str]) -> HelperHandle:
    '''
    ShellExecuteExW with the "runas" verb shows one UAC prompt and starts the
    helper elevated. SEE_MASK_NOCLOSEPROCESS hands back a process handle so
    the lifecycle can poll and terminate it; a declined prompt raises.
    '''
    import ctypes
    from ctypes import wintypes

    SEE_MASK_NOCLOSEPROCESS = 0x00000040
    SW_HIDE = 0

    class SHELLEXECUTEINFOW(ctypes.Structure):
        _fields_ = [
            ("cbSize", wintypes.DWORD),
            ("fMask", ctypes.c_ulong),
            ("hwnd", wintypes.HWND),
            ("lpVerb", wintypes.LPCWSTR),
            ("lpFile", wintypes.LPCWSTR),
            ("lpParameters", wintypes.LPCWSTR),
            ("lpDirectory", wintypes.LPCWSTR),
            ("nShow", ctypes.c_int),
            ("hInstApp", wintypes.HINSTANCE),
            ("lpIDList", ctypes.c_void_p),
            ("lpClass", wintypes.LPCWSTR),
            ("hkeyClass", wintypes.HKEY),
            ("dwHotKey", wintypes.DWORD),
            ("hIcon", wintypes.HANDLE),
            ("hProcess", wintypes.HANDLE),
        ]

    # argv[0] is the executable; the rest are its parameters, quoted.
    params = " ".join(f'"{a}"' for a in argv[1:])
    info = SHELLEXECUTEINFOW()
    info.cbSize = ctypes.sizeof(info)
    info.fMask = SEE_MASK_NOCLOSEPROCESS
    info.lpVerb = "runas"
    info.lpFile = argv[0]
    info.lpParameters = params
    info.nShow = SW_HIDE
    if not ctypes.windll.shell32.ShellExecuteExW(ctypes.byref(info)):
        raise RuntimeError(f"ShellExecuteExW failed (error {ctypes.get_last_error()}) - UAC prompt declined?")
    return _WindowsHandle(info.hProcess)


class _WindowsHandle(HelperHandle):
    def __init__(self, handle):
        self._handle = handle

    def poll(self) -> int | None:
        import ctypes
        WAIT_TIMEOUT = 0x00000102
        if ctypes.windll.kernel32.WaitForSingleObject(self._handle, 0) == WAIT_TIMEOUT:
            return None
        code = ctypes.wintypes.DWORD()
        ctypes.windll.kernel32.GetExitCodeProcess(self._handle, ctypes.byref(code))
        return code.value

    def terminate(self) -> None:
        import ctypes
        try:
            ctypes.windll.kernel32.TerminateProcess(self._handle, 1)
        except Exception:
            pass
