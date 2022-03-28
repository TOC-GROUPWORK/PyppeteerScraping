import re
import requests
import asyncio
from pyppeteer import launch
import os

MAIN_TRUE = 'https://truemoveh.truecorp.co.th/device#'

# MAIN PAGE FOR BRANDS SCRAPING
BRAND_LIST = r'<div class="opt-list " data-name="select_brand" .+</div>'
BRAND_SPAN = r'<span .+</span>'
BRAND_NAME = r'>([a-zA-Z ]+?)<'
# NAME_TEXT = r'[a-zA-Z ]+'

# BRAND PAGE FOR MODELS SCRAPING
# PAGE_NO_BOX = r'<ul class="pg-no-box">((.|\n)*?)</ul>'
PAGE_QUANTITY = r'<span class="hpl-red-txt">[0-9]*</span>'

# MODEL GRID BOX
GRID_BOX = r'<ul id="grid-box" class="box-inner-list-cl clearfix">((.|\n)+?)</ul>'
GRID_FILTER = r'<li class="filter-items".*>((.|\n)+?)</li>'
# MODEL_LINK = r'<a href="https://store.truecorp.co.th/online-store/item/[A-Z0-9]+?\?ln=th">'
MODEL_LINK = r'<a href="(([a-zA-Z0-9]|[-]|[=]|[/]|[?]|[.]|[:])+?)">'
MODEL_NAME = r'class="txt-brand">((.)+?)</a>'

def get_brands(main_url: str) -> list[str]:
     print('GET ALL BRANDS!!!')
     page = requests.get(main_url)
     page.encoding = 'utf-8'

     brands_list = re.findall(BRAND_LIST, page.text)

     brands = []
     for brand in brands_list:
          span = re.findall(BRAND_SPAN, brand)[0]
          brand_name = re.findall(BRAND_NAME, span)[0]
          # name_text = re.findall(NAME_TEXT, brand_name)[0]

          # print(brand_name)
          brands.append(brand_name)

     f= open(f"files/brands.txt","w")
     f.write('\n'.join(brands))
     f.close()

     return brands

async def get_page_quantity(page, brand: str) -> int:
     print('\nGET MODELS AT ' + str.upper(brand) + ' brand!!!')

     uri = 'https://truemoveh.truecorp.co.th/device?search_brand=' + brand + '&search_network=all&page=1'
     # print(uri)

     await page.goto(uri)
     await page.waitFor(500)
     # GET BODY HTML
     page_body = await page.evaluate('() => document.getElementsByTagName("BODY")[0].innerHTML')

     # page = requests.get(uri)
     # page.encoding = 'utf-8'
     # # GET BODY HTML
     # page_body = page.text

     # page_no_box = re.findall(PAGE_NO_BOX, page.text)[0][0]
     # print(page_no_box)

     page_no_box = re.findall(PAGE_QUANTITY, page_body)[0]
     page_quantity = re.findall(r'[0-9]+', page_no_box)[0]
     print(page_quantity)

     # await page.close()
     return int(page_quantity)

async def get_models_at_page(page, brand: str, page_no: int) -> list[str]:
     print('PAGE %d' % page_no)

     uri = 'https://truemoveh.truecorp.co.th/device?search_brand=' + brand + '&search_network=all&page=' + str(page_no)
     print(uri)

     # page = requests.get(uri)
     # page.encoding = 'utf8'
     await page.goto(uri)
     await page.waitFor(500)

     # GET BODY HTML
     page_body = await page.evaluate('() => document.getElementsByTagName("BODY")[0].innerHTML')
     # page_body = page.text

     # <ul id="grid-box" class="box-inner-list-cl clearfix">
     grid_box = re.findall(GRID_BOX, page_body)[0][0]
     # print(grid_box)
     model_list = re.findall(GRID_FILTER, grid_box)

     links = []
     for model in model_list:
          model = model[0]
          # print(model)
          try:
               link = re.findall(MODEL_LINK, model)[0][0]
               name = re.findall(MODEL_NAME, model)[0][0].strip()
          except:
               continue
          links.append(link)
          print(link)
          print(name)

     # print(grid_box)
     print()
     return links

async def get_models(page, brand: str, page_quantity: int):

     print('GET ALL MODELS')
     model_links = []
     for page_no in range(page_quantity):
          model_links += await get_models_at_page(page, brand, page_no + 1)

     f= open(f"files/{brand}.txt","w")
     f.write('\n'.join(model_links))
     f.close()
     return

async def main():
     print("Start TRUE Scraping!!!!")

     db = dict()
     brands = get_brands(MAIN_TRUE)
     
     browser = await launch()
     page = await browser.newPage()
     await page.setViewport({'width': 1920, 'height': 1080})

     for brand in brands:
          page_quantity: int = await get_page_quantity(page, brand)
          await get_models(page, brand, page_quantity)

     await page.close()

asyncio.get_event_loop().run_until_complete(main())