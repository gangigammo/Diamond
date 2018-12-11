from django.test import TestCase

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.common.exceptions import WebDriverException
import os
import pathlib

from .browsers import Browser


# ブラウザのドライバー

class Driver(WebDriver):

    # コンストラクタ

    def __init__(self, browser: Browser):
        self = DriverFactory.new(browser)

    # デストラクタ

    def __del__(self):
        self.close()
        self.quit()


# ドライバーの生成に関する設定

class DriverConfig():
    # ドライバー実行ファイルがあるディレクトリを指定
    bin_dir = '../Diamond/browsers/'
    # OSによって異なる実行ファイルの拡張子
    suffixes = {'nt': '.exe', 'posix': ''}
    # 初めに接続するURLを指定
    default_url = 'http://127.0.0.1:8000'


# ドライバーの生成

class DriverFactory():
    @classmethod
    def new(cls, browser: Browser) -> WebDriver:
        driver = cls.__create_driver(browser)
        cls.__init_driver(driver)
        return driver

    # ドライバーの初期設定をする

    @classmethod
    def __init_driver(cls, driver: Driver):
        # ブラウザ処理の待機時間を設定(seconds)
        driver.implicitly_wait(10)
        # サイトにアクセス
        driver.get(DriverConfig.default_url)

    # 新しいドライバーを生成して返す
    @classmethod
    def __create_driver(cls, browser: Browser) -> WebDriver:
        path = cls.__get_bin_path(browser)
        try:
            driver = browser.factory_method(str(path))
        except WebDriverException:
            message = 'ブラウザ ' + browser.name + ' はインストールされていません.'
            raise EnvironmentError(message)
        return driver

    # ドライバー実行ファイルの絶対パスを取得
    @classmethod
    def __get_bin_path(cls, browser: Browser) -> str:
        relative_path = DriverConfig.bin_dir + browser.bin_path + \
            DriverConfig.suffixes[os.name]
        path = pathlib.Path(relative_path).resolve()

        if (not os.path.exists(path)):
            message = 'ブラウザのドライバ ' + \
                str(path) + ' が存在しません.' + \
                '\n ' + path.name + ' のダウンロード: ' + browser.download_url
            raise EnvironmentError(message)
        return path
