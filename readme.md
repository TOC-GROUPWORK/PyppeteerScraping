pyppeteer
==========

Unofficial Python port of [puppeteer](https://github.com/GoogleChrome/puppeteer) JavaScript (headless) chrome/chromium browser automation library.

* Free software: MIT license (including the work distributed under the Apache 2.0 license)
* Documentation: https://pyppeteer.github.io/pyppeteer/

## Installation

pyppeteer requires Python >= 3.6

Install with `pip` from PyPl:
```bash
pip install pyppeteer
```

Or install the lastest version from [pyppeterr's Git repo](https://github.com/pyppeteer/pyppeteer#pyppeteer):
```bash
pip install -U git+https://github.com/pyppeteer/pyppeteer@dev
```

You have to make sure that `Chrome driver` is in this path.
```
C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe
```

## Usage

Run the command below in this directory to get the brands list in this app.
```cmd
python BrandScraping.py
```

Run the command below in this directory to get information of the phone's promotion.
```bash
python ModelScraping.py
```
