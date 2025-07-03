from setuptools import setup

APP = ['instagram_scraper.py']
DATA_FILES = []
OPTIONS = {
    'argv_emulation': True,
    'packages': ['selenium', 'getpass', 're', 'csv', 'time', 'random', 'platform'],
    # 'iconfile': 'icon.icns', 
}

setup(
    app=APP,
    name="InstagramScraper",
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
