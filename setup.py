from setuptools import setup

APP = ['Instagram_scraper.py']
DATA_FILES = []
OPTIONS = {
    'argv_emulation': True,
    'packages': ['selenium'],  # ONLY third-party packages
    # 'iconfile': 'icon.icns',  # optional icon
}

setup(
    app=APP,
    name="InstagramScraper",
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
