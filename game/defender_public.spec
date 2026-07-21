import os
os.environ["GAME_DEFENDER_ONLY"] = "1"   # set before Analysis() so it's baked into the freeze

from PyInstaller.utils.hooks import collect_data_files, collect_submodules

datas = []
datas += collect_data_files('customtkinter')
datas += [('assets/themes', 'assets/themes')]
datas += [('assets/help_messages.json', 'assets')]
datas += [('assets/presets/dev.json', 'assets/presets')]

hiddenimports = []
hiddenimports += collect_submodules('customtkinter')
hiddenimports += ['matplotlib.backends.backend_tkagg']

a = Analysis(
    ['main.py'],              # ← was main_defender.py, now points at the real entry point
    pathex=['.'],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    runtime_hooks=['hooks/rthook_defender_only.py'], 
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data)

exe = EXE(
    pyz, a.scripts, a.binaries, a.zipfiles, a.datas, [],
    name='DefenderClient',
    console=True,
    upx=True,
)