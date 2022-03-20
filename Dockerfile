FROM python:3.9
WORKDIR /pyppeteer
RUN pip install -U git+https://github.com/pyppeteer/pyppeteer@dev
EXPOSE 8000
COPY . /pyppeteer
CMD ["python", "src/app.py"]