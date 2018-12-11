from django.test import TestCase
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

from .drivers import Drivers
from .drivers import Browser

# Create your tests here.``


def new():
    try:
        driver = Drivers.new(Browser.Chrome)
    except Exception as e:
        print(e)
        message = 'テスト用ブラウザを初期化できませんでした.'
        print(message)
        raise SystemExit(message)

    # ブラウザ処理の待機時間を設定(seconds)
    driver.implicitly_wait(10)
    # サイトにアクセス
    driver.get('http://127.0.0.1:8000')
    return driver
