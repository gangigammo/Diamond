from django.test import TestCase
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from .drivers import Drivers
from .drivers import Browser

# Create your tests here.``


def test_sample():
    try:
        driver = Drivers.get(Browser.Chrome)
    except Exception as e:
        print(e)
        message = 'テスト用ブラウザを初期化できませんでした.'
        print(message)
        raise SystemExit(message)
    driver.implicitly_wait(10)  # ブラウザ処理の待機時間(seconds)
    driver.get('http://127.0.0.1:8000')
    driver.find_element_by_xpath("/html/body/a").click()
    driver.close()
    driver.quit()
