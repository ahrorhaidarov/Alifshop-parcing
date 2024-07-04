import asyncio
import time

import pandas as pd

from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()



def get_product_data(product_url):
    driver.get(product_url)
    product_dict = {}
    product_dict['link'] = product_url

    product_name = driver.find_element(By.XPATH, "//div/h1[@class='text-xl text-black leading-8 mb-1']").text
    product_dict['product_name'] = product_name

    price = driver.find_element(By.XPATH, "//div/p[@class='text-2xl font-family-bold']").text
    product_dict['price'] = price

    instalment = driver.find_element(By.XPATH, "//div/p[@class='text-gray-500 text-lg']").text
    product_dict['instalment'] = instalment

    specifications = driver.find_elements(By.XPATH, "//li[@class='mb-1']")
    for specification in specifications:
        key = specification.find_element(By.XPATH, ".//span[@class='text-gray-500 text-base leading-5 mr-1']").text
        value = specification.find_element(By.XPATH, ".//span[@class='text-base leading-5']").text
        product_dict[key] = value

    return product_dict

async def get_all_products(url):
    driver.get(url)
    links = list()
    for product in driver.find_elements(By.XPATH, "//div[@class='relative w-min']/a"):
        link = product.get_attribute('href')
        links.append(link)
    return links


async def page_range(category_url):
    product_links = list()
    driver.get(category_url)
    last_page = driver.find_element(By.XPATH,
                            "//button[@class='inline-block text-gray-500 border-2 border-transparent rounded-md hover:text-primary-200 focus:outline-none py-2 px-3.5']").text
    for page in range(1, int(last_page)+1):
        links = await get_all_products(f"{category_url}?page={page}")
        product_links.extend(links)
    return product_links
def export(all_product_data, file_path):
    all_keys = set()
    for i in all_product_data:
        for key in i.keys():
            all_keys.add(key)

    data_dict = dict()
    for key in all_keys:
        data_dict[key] = list()

    for product_dict in all_product_data:
        for key in all_keys:
            try:
                data_dict[key].append(product_dict[key])
            except KeyError:
                print(key, product_dict)
                data_dict[key].append(None)
    df = pd.DataFrame.from_dict(data_dict)
    df.to_excel(file_path, index=False)
    print('Export complete')
    return df

def main(url, exoprt_path):
    all_product_data = list()
    product_links = asyncio.run(page_range(url))
    for link in product_links:
        product_data = get_product_data(link)
        all_product_data.append(product_data)

    export(all_product_data, exoprt_path)


url = "https://alifshop.tj"

def categories(url):
    driver.get(url)
    catalog_button = driver.find_element(By.XPATH, "//button[@aria-label='Catalog']")
    catalog_button.click()
    time.sleep(2)
    categories = driver.find_elements(By.XPATH,
                                      "//div[@class='relative left-side py-5 bg-gray-200 block z-10']//li/a[contains(@href, '/category')]")
    return categories

categoriess = categories(url)

for category in categoriess[2:]:
    category_url = category.get_attribute("href")
    main(url=category_url, exoprt_path=f"{category.text}.xlsx")