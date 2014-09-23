import sys
from cx_Freeze import setup, Executable

includefiles = ['ContentDictionaryInitialization.py']
excludes = ['Tkinter']
packages = ['os','re','urllib.request','sys','collections']

setup(
    name = "ContentDictionaryInitializationExe",
    version = "1.0",
    description = "Builds initialization entries from the content dictionary report.",
    options = {'build_exe': {'excludes':excludes,'packages':packages,'include_files':includefiles}},
    executables = [Executable("run.py", base = "Win32GUI")])