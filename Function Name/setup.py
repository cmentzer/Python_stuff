import sys
from cx_Freeze import setup, Executable

includefiles = ['GetFunctionNames.py']
excludes = ['Tkinter']
packages = ['os','re','urllib.request','sys','collections']

setup(
    name = "GetFunctionNamesExe",
    version = "1.0",
    description = "Retrieves all of the functions from the M-AT wiki.",
    options = {'build_exe': {'excludes':excludes,'packages':packages,'include_files':includefiles}},
    executables = [Executable("run.py", base = "Win32GUI")])