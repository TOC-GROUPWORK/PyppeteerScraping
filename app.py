import asyncio
from pyppeteer import launch
from bs4 import BeautifulSoup
import os

async def main():
    browser = await launch({'defaultViewport': {'width': 1960, 'height': 1680}})
    page = await browser.newPage()
    await page.goto('https://truemoveh.truecorp.co.th/device#')

    await page.click('div.brand-opts')
    brands = await page.evaluate('''
        () => {
            const brands = document.querySelectorAll('div.brand-opts div.option-list-group div.opt-list span.opt-txt')
            const brandlst = Array.from(brands).map(brand => brand.innerHTML)
            return brandlst
        }
    ''')

    print(brands)
    await page.screenshot({ 'path': 'main.png', 'fullPage': True})

    for brand in brands[1:]:

        uri = 'https://truemoveh.truecorp.co.th/device?search_brand=' + brand + '&search_network=all&page=1'
        os.mkdir(os.getcwd() + '/Screenshot/' +brand)
        await page.goto(uri)
        # await page.waitFor(500)

        number_of_pages = await page.evaluate('''
            () => {
                const number = document.querySelectorAll('li.load-ajx-data.paging-max span.hpl-red-txt')
                const numberlst = Array.from(number).map(n => n.innerHTML)
                return numberlst[0]
            }
        ''')

        # all_links = []

        i = 0
        while(i < int(number_of_pages)):
            path = '/Screenshot/' + brand + '/page_' + str(i) + '.png'
            await page.screenshot({'path': path, 'fullPage' : True})
        #     page_links = await page.evaluate('''
        #         () => {
        #             const links = document.querySelectorAll('a.txt-brand')
        #             const urls = Array.from(links).map(link => link.href)
        #             return urls
        #         }
        #     ''')

        #     all_links += page_links 
            
            await page.click('div.ajx-pg-btn.ajx-pg-next.pg-right-arw')
            await page.waitFor(2000)
            i += 1

        # for l in all_links:
        #     print(l)
    await browser.close()

asyncio.get_event_loop().run_until_complete(main())