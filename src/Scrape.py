import asyncio
from pyppeteer import launch
import os
from bs4 import BeautifulSoup
import json

async def Scrape():

    browser = await launch()
    page = await browser.newPage()
    await page.setViewport({'width':  1920, 'height': 1080, 'isLandscape': True})

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
            await page.goto(url, { 'waitUntil': 'networkidle0' }) 
            # await page.waitForSelector(selector = 'div.stickyProb', options = { 'visible': True, 'timeout': 60000 })

        # Pictures
            # pictures = await page.evaluate('''
            #     () => {
            #         const stickyProb = document.querySelectorAll('img.carousel')
            #         const pictures = Array.from(stickyProb).map(p => p.src)
            #         return pictures
            #     }
            # ''')
            # # print(pictures)
            # for p in pictures:
            #     print(p) 

            try:
                content = await page.evaluate('''
                    () => {
                        var content = {}
                        
                        const model = document.querySelector('div.flex.justify-between div.text-4xl.font-bold.text-black')
                        content.model = model.innerText

                        const stickyProb = document.querySelectorAll('img.carousel')
                        content.pictures = Array.from(stickyProb).map(p => p.src)
                        
                        const colors = document.querySelectorAll('div.rounded-full.shadow-inset')
                        content.colors = Array.from(colors).map((color) => {
                            var elementStyle = color.style;
                            var computedStyle = window.getComputedStyle(color, null)
                            var prop = 'background-color'

                            if (elementStyle.hasOwnProperty(prop))
                                return computedStyle[prop]
                            else
                                return 'rgb(255, 255, 255)'
                        })

                        const color_names = document.querySelectorAll('label.w-full.break-word')
                        content.color_names = Array.from(color_names).map(name => name.innerText)

                        const rams = document.querySelectorAll('div.relative button.p-4')
                        content.rams = Array.from(rams).map(ram => ram.innerText)

                        const detail_boxs = document.querySelectorAll('div.flex-auto > div')
                        content.detail = Array.from(detail_boxs).map(p => p.innerHTML)

                        return content
                    }
                ''')
            except Exception as e: 
                print(str(e))
                continue

            div_elements = len(content.get('detail'))
            del content['detail']
            print()

            content['url'] = url
            page_n = 0 
            content['promotions'] = {}
            while (True):
                
                # promotions = await page.querySelectorAll('div.flex-auto > div')
                # selector = 'div.flex-auto > div:nth-child(' + div + ') > div > button > div'
                # print(type(promotions))
                
                promotions = await page.evaluate('''
                    () => {
                        const detail_boxs = document.querySelectorAll('div.flex-auto > div')
                        const div = Array.from(detail_boxs).map(p => p.innerHTML).length - 5

                        const selector = 'div.flex-auto > div:nth-child(' + div + ') > div > button > div'
                        const promotions = document.querySelectorAll(selector)
                        
                        return Array.from(promotions).map(promotion => promotion.innerText)
                    }
                ''')
                ram = content['rams'][page_n]
                content['promotions'][ram] = []
                for index, p in enumerate(promotions):
                    # print(type(p))
                    content['promotions'][ram].append({ 'promotion' : p.split('\n')})
                    # print(content['promotions'][-1])

                    payment = await page.evaluate('''
                        () => {
                            const selector = 'div.flex-auto > div.grid.scroll-container.text-22 > div > div'
                            const payments = document.querySelectorAll(selector)

                            return Array.from(payments).map(payment => payment.innerText)
                        }
                    ''')

                    content['promotions'][ram][-1]['payments'] = payment
                    # print('\t', content['promotions'][-1])

                    packages = await page.evaluate('''
                        () => {
                            const detail_boxs = document.querySelectorAll('div.flex-auto > div')
                            const div = Array.from(detail_boxs).map(p => p.innerHTML).length - 1

                            const selector = 'div.flex-auto > div:nth-child(' + div + ') > div > button'
                            const packages = document.querySelectorAll(selector)

                            return Array.from(packages).map(package => package.innerText)
                        }
                    ''')

                    content['promotions'][ram][-1]['packages'] = []
                    for package in packages:
                        content['promotions'][ram][-1]['packages'].append({ 'package': package.split('\n') })
                        details = await page.evaluate('''
                            () => {
                                const details = []
                                const detail_boxs = document.querySelectorAll('div.flex-auto > div')
                                const div = Array.from(detail_boxs).map(p => p.innerHTML).length

                                let selector = 'div.package-name-container > button > div > div.package-name'
                                let names = document.querySelectorAll(selector)
                                names = Array.from(names).map(name => name.innerText)

                                selector = 'div.option_container.flex > div > div > p:nth-child(2) > img'
                                let images = document.querySelectorAll(selector)
                                images = Array.from(images).map(img => img.src)

                                for (let index = 0; index < names.length; index++) {
                                    const detail = {}
                                    detail.name = names[index]
                                    detail.picture = images[index]
                                    details.push(detail)
                                }

                                return details
                            }
                        ''')

                        content['promotions'][ram][-1]['packages'][-1]['details'] = details
                        # print(content['promotions'][-1])

                        # for 
                        # print('\t\t\t', details)
                        # print()

                    # print('\t\t',packages)
                    # print()
                    # exit(1)
                page_n += 1
                if page_n >= len(content.get('rams')):
                    break

            json_string = json.dumps(content, indent=4, ensure_ascii=False).encode('utf8')

            f = open('src/Screenshot/' + brand + '/pages/' + content['model'].replace('/','-') + '.txt',"w+", encoding='utf-8')
            f.write(json_string.decode())
            f.close()

            # print(json_string.decode())
            exit(1)


            # for index in range(1, len(content['rams']) + 1):
                # detail
                # div.flex-auto > div:nth-child(11) > div > div
                # package
                # div.flex-auto > div:nth-child(6) > div > button:nth-child(2)
                # payment
                # div.flex-auto > div.grid.scroll-container.text-22 > div > div
                # promotion
                # div.flex-auto > div:nth-child(4) > div > button
                # div.flex-auto > div:nth-child(2) > div > button:nth-child(2) > div
                # ram
                # await page.click('div:nth-child(4) > div:nth-child(%d) > button' % index)
                # 
            
        # Model
            # try:
            #     model = await page.evaluate('''
            #         () => {
            #             const  = document.querySelector('div.flex.justify-between div.text-4xl.font-bold.text-black')
            #             return model.innerHTML
            #         }
            #     ''')
            # except:
            #     try:
            #         model = await page.evaluate('''
            #             () => {
            #                 const model = document.querySelector('div.acd-hdr-inner div strong')
            #                 return model.innerText
            #             }
            #         ''')
            #     except:
            #         continue

            # print(model if model else index)
            # path = 'src/Screenshot/' + brand + '/pages/' + str(index) + '.png'
            # print(path)
            # await page.screenshot({'path': path})
            # await page.pdf({'path': path})
        print()

    await browser.close()

asyncio.get_event_loop().run_until_complete(Scrape())