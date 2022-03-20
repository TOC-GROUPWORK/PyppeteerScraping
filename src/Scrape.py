import asyncio
from pyppeteer import launch
import os

async def Scrape():

    browser = await launch()
    page = await browser.newPage()
    await page.setViewport({'width': 1920, 'height': 1080, 'isLandscape': True})

    f = open('src/brands.txt', 'r')
    brands = []
    for brand in f:
        brands.append(brand.split('\n')[0])
    f.close()

    for brand in brands:
        print(brand)

        dir = os.getcwd() + '/src/Screenshot/%s/pages' % (brand)
        if not os.path.exists(dir):
            os.mkdir(dir)

        f = open('src/Screenshot/%s/urls.txt' % (brand), 'r')
        urls = []
        for index, url in enumerate(f):
            urls.append(url.split('\n')[0])
        f.close()

        for index, url in enumerate(urls):
            print(url)
            await page.goto(url) 
            await page.waitFor(7000)

            path = 'src/Screenshot/' + brand + '/pages/' + str(index) + '.png'
            print(path)
            await page.screenshot({'path': path})

        print()



    return

asyncio.get_event_loop().run_until_complete(Scrape())