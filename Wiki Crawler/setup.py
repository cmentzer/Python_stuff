import sys
from cx_Freeze import setup, Executable

includefiles = ['input.txt','Snippet_Generation.py','Wiki_Crawler.py']
excludes = ['Tkinter']
packages = ['os','re','urllib.request','sys','collections']

setup(
    name = "Snippet Builder",
    version = "1.0",
    description = "Builds sublimetext snippets from M-AT wiki.",
    options = {'build_exe': {'excludes':excludes,'packages':packages,'include_files':includefiles}},
    executables = [Executable("Run_Crawler.py", base = "Win32GUI")])