import os
import sys
os.environ['TCL_LIBRARY'] = "C:\\Users\\trhrtnj\\AppData\\Local\\Programs\\Python\\Python36-32\\tcl\\tcl8.6"
os.environ['TK_LIBRARY'] = "C:\\Users\\trhrtnj\\AppData\\Local\\Programs\\Python\\Python36-32\\tcl\\tk8.6"

include_files = [r"C:\Users\trhrtnj\AppData\Local\Programs\Python\Python36-32\DLLs\tcl86t.dll",
					r"C:\Users\trhrtnj\AppData\Local\Programs\Python\Python36-32\DLLs\tk86t.dll"]

from cx_Freeze import setup, Executable

base = None
if (sys.platform == "win32"):
	base = "Win32GUI"    # Tells the build script to hide the console.

build_exe_options = {"packages": ["os", "tkinter"], "excludes": []}
executables = [Executable("csvBake.py", base=base,  icon='icon.ico')]

packages = []
options = {
	'build_exe': {
		'packages':packages,
		'include_files': include_files
	},
}

setup(
    name = 'PrestaShop CSV Baker',
    options = options,
    version = '1.0',
    description = 'PrestaShop CSV import helper',
    executables = executables
)