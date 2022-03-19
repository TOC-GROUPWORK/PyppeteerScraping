FROM python:3.8

RUN pip install pyppeteer
RUN pip install -U git+https://github.com/pyppeteer/pyppeteer@dev