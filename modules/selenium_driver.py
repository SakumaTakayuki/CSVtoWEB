from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os


def init_driver(headless=True):
    options = Options()
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--start-maximized")

    if headless:
        options.add_argument("--headless=new")

    chrome_path = os.getenv("CHROME_DRIVER_PATH", "")
    if chrome_path and os.path.exists(chrome_path):
        service = Service(executable_path=chrome_path)
    else:
        service = Service()

    driver = webdriver.Chrome(service=service, options=options)

    driver.implicitly_wait(3)

    return driver


def wait_for(driver, by: By, value: str, timeout: int = 10):
    return WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((by, value))
    )
