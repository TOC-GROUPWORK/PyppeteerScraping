import asyncio
from pyppeteer import launch
import os

async def main():
    browser = await launch()
    page = await browser.newPage()
    await page.setViewport({'width': 1920, 'height': 1080})
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
    f = open('src/brands.txt',"w+")
    for brand in brands[1:]:
        f.write(brand + '\n')
    f.close()

    await page.screenshot({ 'path': 'src/main.png', 'fullPage': True})

    for brand in brands[1:]:

        uri = 'https://truemoveh.truecorp.co.th/device?search_brand=' + brand + '&search_network=all&page=1'
        
        if not os.path.exists(os.getcwd() + '/src/Screenshot/' + brand):
            os.mkdir(os.getcwd() + '/src/Screenshot/' + brand)
        
        await page.goto(uri)
        await page.waitFor(500)

        number_of_pages = await page.evaluate('''
            () => {
                const number = document.querySelectorAll('li.load-ajx-data.paging-max span.hpl-red-txt')
                const numberlst = Array.from(number).map(n => n.innerHTML)
                return numberlst[0]
            }
        ''')

        all_links = []
        
        i = 0
        while(i < int(number_of_pages)):
            await page.waitForSelector('div.block-inner-main')
            path = 'src/Screenshot/' + brand + '/page_' + str(i) + '.png'
            await page.screenshot({'path': path, 'fullPage' : True})
            page_links = await page.evaluate('''
                () => {
                    const links = document.querySelectorAll('a.txt-brand')
                    const urls = Array.from(links).map(link => link.href)
                    return urls
                }
            ''')

            all_links += page_links 
            
            await page.click('div.ajx-pg-btn.ajx-pg-next.pg-right-arw')
            await page.waitFor(2000)
            i += 1

        f = open('src/Screenshot/' + brand + '/urls.txt',"w+")
        for l in all_links:
            f.write(l + '\n')
        f.close()
        print('FINISHED : ' + brand)
    await browser.close()

asyncio.get_event_loop().run_until_complete(main())