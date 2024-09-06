from setuptools import setup
import os

def collect_assets():
    data_files = []
    asset_dirs = ['data', 'assets/background', 'assets/music', 'assets/balls', 'assets/names', 'assets/sounds', 'assets/icons', 'assets/cries', 'assets/sprites', 'assets/font', 'assets/sugimori_mini']  # Add other asset directories here
    for directory in asset_dirs:
        for dirpath, _, filenames in os.walk(directory):
            for filename in filenames:
                file_path = os.path.join(dirpath, filename)
                relative_dir = os.path.relpath(dirpath, 'assets')
                data_files.append((os.path.join('assets', relative_dir), [file_path]))
    return data_files

DATA_FILES = collect_assets()

APP = ['main.py']  # Replace with your main script
#DATA_FILES = ['data', 'assets/background', 'assets/music', 'assets/balls', 'assets/names', 'assets/sounds', 'assets/icons', 'assets/cries', 'assets/sprites', 'assets/font', 'assets/sugimori_mini']

OPTIONS = {
    'argv_emulation': False,
    'packages': ['pygame', 'numpy'],
    'includes': ['pokemon', 'session', 'config', 'sprites', 'utils'],  # Include other modules used
    'excludes': ['PyQt5', 'PySide2', 'tkinter','gi.repository', 'GstTag','packaging'],
    'plist': {
        'CFBundleName': 'Poke Typing',  # The name of the app
        'CFBundleIconFile': 'icon.icns',  # The name of the icon file
    },
    'iconfile': 'icon.icns',  # The icon file to use
    'frameworks': ['/usr/local/Cellar/libffi/3.4.6/lib/libffi.8.dylib']
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
