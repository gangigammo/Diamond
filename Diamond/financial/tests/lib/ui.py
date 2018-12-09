from django.test import TestCase
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from enum import IntEnum, auto
import os
import pathlib

# Create your tests here.``

# ブラウザの列挙


class Browser(IntEnum):
    Chrome = auto()
    Edge = auto()
    Firefox = auto()

# ブラウザのドライバーを新しく取得する


class Drivers:
    # ドライバーがあるパスを指定
    dir_path = '../Diamond/browsers/'
    # ドライバー本体のファイル名を指定
    bin_paths = {Browser.Chrome: 'chromedriver',
                 Browser.Edge: 'MicrosoftWebDriver',
                 Browser.Firefox: 'geckodriver'}

    # ダウンロードURLのメモ
    bin_urls = {
        Browser.Chrome: 'https://sites.google.com/a/chromium.org/chromedriver/downloads',
        Browser.Edge: 'https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/',
        Browser.Firefox: 'https://github.com/mozilla/geckodriver/releases'}
    # ドライバーの取得関数
    factories = {Browser.Chrome: webdriver.Chrome,
                 Browser.Edge: webdriver.Edge,
                 Browser.Firefox: webdriver.Firefox}
    # OSによって異なる実行ファイルの拡張子
    suffix = {'nt': '.exe', 'posix': ''}

    # テスト用ブラウザを取得する
    @classmethod
    def get(cls, browser: Browser):
        path = cls.dir_path + cls.bin_paths[browser] + cls.suffix[os.name]
        abs_path = pathlib.Path(path).resolve()
        if (os.path.exists(abs_path)):
            try:
                driver = cls.factories[browser](str(abs_path))
            except WebDriverException:
                message = 'ブラウザ ' + browser.name + ' はインストールされていません.'
                raise EnvironmentError(message)
        else:
            message = 'ブラウザのドライバ ' + \
                str(abs_path) + ' が存在しません.' + \
                '\n ' + abs_path.name + ' のダウンロード: ' + cls.bin_urls[browser]
            raise FileNotFoundError(message)
        return driver


def test_sample():
    try:
        driver = Drivers.get(Browser.Chrome)
    except Exception as e:
        print(e)
        message = 'テスト用ブラウザを初期化できませんでした.'
        print(message)
        raise SystemExit(message)
    driver.implicitly_wait(10)  # seconds
    driver.get('http://127.0.0.1:8000')
    driver.find_element_by_xpath("/html/body/a").click()
    driver.close()
    driver.quit()


def sample():
    print('unko')
