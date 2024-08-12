import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup


def init_webdriver(chrome_driver_path, headless=True):
    """Initialize the Chrome WebDriver."""
    chrome_options = Options()
    if headless:
        chrome_options.add_argument("--headless")  # Run in headless mode
    service = Service(chrome_driver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def get_page_source(driver, url):
    """Get the page source HTML."""
    driver.get(url)
    time.sleep(5)  # Wait for the page to load
    return driver.page_source

def extract_names_prices(soup):
    """Extract product names and prices from the HTML soup."""
    products = {}
    for product in soup.find_all('div', class_='product-item'):
        name_tag = product.find('h4', class_='title')
        price_tag = product.find('div', class_='price-regular')
        discount_tag = product.find('div', class_='price-discount-regular')
        discount_circle = product.find('div', class_='discount')

        if name_tag and price_tag:
            name = name_tag.text.strip()
            price = price_tag.find_all('span')[-1].text.strip()
            discount = None
            products[name] = {"price": price, "discount": discount}
        elif name_tag and discount_tag:
            name = name_tag.text.strip()
            price = discount_tag.find('div').text.strip()
            discount = discount_circle.text.strip() if discount_circle else None
            products[name] = {"price": price, "discount": discount}
    return products
