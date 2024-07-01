import time

from selenium import webdriver
from selenium.webdriver.common.by import By
import numpy as np
import requests
from bs4 import BeautifulSoup
from tempfile import TemporaryFile

from lxml import etree


outfile = TemporaryFile()

url = "https://alifshop.tj"


driver = webdriver.Chrome()
driver.get(url)
# wait = WebDriverWait(driver, timeout=10)

catalog_button = driver.find_element(By.XPATH, "//button[@aria-label='Catalog']")
catalog_button.click()


categories = driver.find_elements(By.XPATH, "//div[@class='relative left-side py-5 bg-gray-200 block z-10']//li/a[contains(@href, '/category')]")


data = list()


def get_data(product_url):
    req = requests.get('https://alifshop.tj/product/samsung-galaxy-a54-5g-8-256-gb-chernyy')
    soup = BeautifulSoup(req.content, 'html.parser')
    dom = etree.HTML(str(soup))

    product_name = dom.xpath("//div/p[@class='text-2xl font-family-bold']")


    product_dict = dict()
    try:

        product_dict['product_name'] = product_name
        print(product_name)
    except:
        print("product error")

    try:
        price = driver.find_element(By.XPATH, "//div/p[@class='text-2xl font-family-bold']").text
        product_dict['price'] = price
    except:
        print("price error")

    try:
        instalment = driver.find_element(By.XPATH, "//div/p[@class='text-gray-500 text-lg']").text
        product_dict['instalment'] = instalment

    except:
        print("instalment error")

    try:
        specifications = driver.find_elements(By.XPATH, "//li[@class='mb-1']")
        for specification in specifications:
            key = specification.find_elements(By.XPATH, "//span[@class='text-gray-500 text-base leading-5 mr-1']")
            value = specification.find_elements(By.XPATH, "//span[@class='text-base leading-5']")
            for i, j in zip(key, value):
                product_dict[i.text] = j.text
        data.append(product_dict)
        driver.back()
        time.sleep(1)
    except Exception as e:
        print(e)



def click_catalog_button(category_url):
    driver.get(category_url)
    products = driver.find_elements(By.XPATH, "//div[@class='relative w-min']/a")
    print('Products found')
    i = 0
    while i < len(products):
        print('Length of products', len(products), i)
        products = driver.find_elements(By.XPATH, "//div[@class='relative w-min']/a") #В корзину
        prduct_url = products[i].get_attribute('href')
        time.sleep(1)
        get_data(prduct_url)
        i += 1




def page_range(category_url):
    driver.get(category_url)
    print('Searching for last page')
    last_page = driver.find_element(By.XPATH,
                            "//button[@class='inline-block text-gray-500 border-2 border-transparent rounded-md hover:text-primary-200 focus:outline-none py-2 px-3.5']").text

    for page in range(1, int(last_page) + 1):
        print('PAge', page)
        click_catalog_button(category_url + "?page=" + str(page))

for category in categories[1:]:
    print(category)
    link = category.get_attribute('href')
    page_range(link)



np.save(outfile, np.array(data))