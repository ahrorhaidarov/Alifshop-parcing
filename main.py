import time
from selenium import webdriver
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup


url = "https://alifshop.tj"
driver = webdriver.Chrome()
driver.get(url)


categories = driver.find_elements(By.XPATH, "//div[@class='relative left-side py-5 bg-gray-200 block z-10']//li/a[contains(@href, '/category')]")[1:]

def get_data():
    product_dict = {}
    try:
        product_name = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//div/h1[@class='text-xl text-black leading-8 mb-1']")).text
        product_dict['product_name'] = product_name
    except:
        print("product error")

    try:
        price = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//div/p[@class='text-2xl font-family-bold']"))).text
        product_dict['price'] = price
    except:
        print("price error")

    try:
        instalment = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//div/p[@class='text-gray-500 text-lg']"))).text
        product_dict['instalment'] = instalment
    except:
        print("instalment error")

    try:
        specifications = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, "//li[@class='mb-1']")))
        for specification in specifications:
            key = specification.find_element(By.XPATH, ".//span[@class='text-gray-500 text-base leading-5 mr-1']").text
            value = specification.find_element(By.XPATH, ".//span[@class='text-base leading-5']").text
            product_dict[key] = value
        data.append(product_dict)
        driver.back()
        time.sleep(1)
    except Exception as e:
        print(e)


def click_catalog_button(category_url):
    driver.get(category_url)
    print('Products found')

    while True:
        products = driver.find_elements(By.XPATH, "//div[@class='relative w-min']/a")
        if not products:
            break

        for product in products:
            try:
                product.click()
            except ElementClickInterceptedException:
                print('Element Click Intercepted')
                continue
            time.sleep(1)
            get_data()

            # Refresh the products list to avoid StaleElementReferenceException
            products = driver.find_elements(By.XPATH, "//div[@class='relative w-min']/a")

def page_range(category_url):
    driver.get(category_url)
    print('Searching for last page')
    last_page = driver.find_element(By.XPATH,
                                    "//button[@class='inline-block text-gray-500 border-2 border-transparent rounded-md hover:text-primary-200 focus:outline-none py-2 px-3.5']").text

    for page in range(1, int(last_page) + 1):
        print('Page', page)
        click_catalog_button(category_url + "?page=" + str(page))

for category in categories:
    link = category.get_attribute('href')
    page_range(link)
