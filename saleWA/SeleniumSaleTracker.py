"""
@Today's Date : 2/27/2023

@Author : Thomas Barker
"""
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from PIL import Image
import re


def check_sales(links):
    options = Options()
    options.add_argument('--headless')
    user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.517 Safari/537.36'
    options.add_argument('user-agent={0}'.format(user_agent))

    for link in links:
        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options)
        driver.get(link)

        driver.implicitly_wait(10)


        window_height = driver.execute_script(
            'return Math.max( document.body.scrollHeight, document.body.offsetHeight, document.documentElement.clientHeight, document.documentElement.scrollHeight, document.documentElement.offsetHeight );')
        driver.set_window_size(1920, window_height / 3)
        driver.implicitly_wait(10)

        item_name = driver.find_element(By.CSS_SELECTOR, 'h1')
        print(item_name.text)

        print(link)

        item_prices = driver.find_elements(By.CSS_SELECTOR, "*[class*=pric]")
        lowest_price = 99999999
        for element in item_prices:
            text = element.text
            price = re.search(r"\$\d+", text)
            if price:
                intprice = int(price.group()[1:])
                if intprice < lowest_price:
                    lowest_price = intprice
        print("$" + str(lowest_price))

        with open('ss.png', 'wb') as f:
            f.write(driver.get_screenshot_as_png())
        img = Image.open('ss.png')
        img.show()
        driver.quit()

        
urls = ["https://bearbottomclothing.com/collections/shorts/products/loft"
        "-short",
        "https://www.patagonia.com/product/mens-hemp-work-sweatshirt"
        "/21399.html?cgid=mens-fleece",
        "https://www.abercrombie.com/shop/us/p/textured-stitch-crew"
        "-sweater-51918825?seq=03&categoryId=86655&faceout=model",
        "https://www.patagonia.com/product/mens-long-sleeved-cotton-in"
        "-conversion-lightweight-fjord-flannel-shirt/42410.html?dwvar_42410_color=BETB&cgid=web-specials-mens",
        "https://unitedbyblue.com/products/mens-indigo-throwback"
        "-sweatshirt",
        "https://bananarepublicfactory.gapfactory.com/browse/product.do"
        "?pid=580739001&cid=1045334&pcid=1045334&vid=1&nav=meganav%3AMen%3AMen%27s+Clothing%3ASweaters&cpos=18&cexp=368&kcid=CategoryIDs%3D1045334&cvar=2363&ctype=Listing&cpid=res23021722208407532520781#pdp-page-content"]

check_sales(urls)
    


