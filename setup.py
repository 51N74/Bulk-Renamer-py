# -*- coding: utf-8 -*-
from setuptools import setup

APP = ['bulk_rename_gui.py']
DATA_FILES = []
OPTIONS = {
    'argv_emulation': True,
    'plist': {
        'CFBundleName': 'File Renamer',
        'CFBundleDisplayName': 'File Renamer',
        'CFBundleGetInfoString': "Bulk file renaming utility",
        'CFBundleIdentifier': "com.filerenamer.app",
        'CFBundleVersion': "1.0.0",
        'CFBundleShortVersionString': "1.0.0",
        'NSHumanReadableCopyright': "Copyright © 2024, Your Name, All Rights Reserved"
    },
    'packages': ['tkinter'],
    # 'iconfile': 'app_icon.icns'  # If you have an icon file
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)