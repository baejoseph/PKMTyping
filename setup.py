from setuptools import setup

APP = ['main.py']  # Replace with your main script
DATA_FILES = ['assets', 'data', 'font']  # Add other directories or files needed
OPTIONS = {
    'argv_emulation': True,
    'packages': ['pygame', 'numpy'],
    'includes': ['pokemon', 'session', 'config', 'sprites'],  # Include other modules used
    'plist': {
        'CFBundleName': 'Poke Typing',  # The name of the app
        'CFBundleIconFile': 'icon.icns',  # The name of the icon file
    },
    'iconfile': 'icon.icns',  # The icon file to use
    'frameworks': ['/usr/local/anaconda3/envs/pokemon-typing/lib/libffi.8.dylib']
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
