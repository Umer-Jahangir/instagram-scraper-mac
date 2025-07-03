# Instagram Scraper (macOS App)

A simple macOS desktop application that scrapes Instagram data using Python and Selenium.

This app is packaged as a `.app` and distributed via a `.dmg` file using GitHub Actions and `py2app`.

## Features

- Login to Instagram (headless or visible)
- Scrape data (followers, posts, etc.)
- Export results to CSV
- Built with: `Python`, `Selenium`, `webdriver-manager`
- Packaged for macOS using `py2app`

## How to Use

1. Download the `.dmg` file from [Releases](https://github.com/Umer-Jahangir/instagram-scraper-mac/actions) or from the GitHub Actions artifacts.
2. Open the `.dmg` and drag `InstagramScraper.app` to your Applications folder.
3. Run the app — you may need to allow it in **System Preferences > Security & Privacy** if macOS warns about it.
4. Follow the on-screen instructions or command line prompts.

## Development

To build the app manually:

```bash
pip install -r requirements.txt
pip install py2app
python setup.py py2app

```

To create a `.dmg` file:

```bash
hdiutil create -volname InstagramScraper \
  -srcfolder "dist/InstagramScraper.app" \
  -ov -format UDZO InstagramScraper.dmg
```

## GitHub Actions Build

This repo uses GitHub Actions to:

- Build the macOS `.app` from Python script

- Package it into a `.dmg`

- Upload the `.dmg` as an artifact

Check `.github/workflows/mac_build.yml` for workflow details.

## Project Structure

```bash
.
├── instagram_scraper.py      # Main app logic
├── setup.py                  # py2app setup
├── requirements.txt          # Python dependencies
├── README.md                 # You're reading it!
└── .github/workflows/
    └── mac_build.yml         # GitHub Actions CI config
```
## Requirements

- macOS (for using the built `.dmg`)

- Python 3.11+ (for development)

- Chrome + ChromeDriver (managed by `webdriver-manager`)

## License

This project is for educational and personal use only. Use at your own risk. Instagram scraping may violate their terms of service.


