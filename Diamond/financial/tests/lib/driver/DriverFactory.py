
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.common.exceptions import WebDriverException
import os
import pathlib

from .browser import Browser
from . import DriverConfig


# 新しいドライバーを生成し、初期設定して返す

def new(browser: Browser) -> WebDriver:
    driver = __create_driver(browser)
    # ブラウザ処理の待機時間を設定(seconds)
    driver.implicitly_wait(DriverConfig.wait_time)
    # サイトにアクセス
    driver.get(DriverConfig.default_url)
    return driver


# 新しいドライバーを生成して返す

def __create_driver(browser: Browser) -> WebDriver:
    path = __get_bin_path(browser)
    try:
        driver = browser.factory_method(str(path))
    except WebDriverException:
        message = 'ブラウザ ' + browser.name + ' はインストールされていません.'
        raise EnvironmentError(message)
    return driver


# ドライバー実行ファイルの絶対パスを取得

def __get_bin_path(browser: Browser) -> str:
    base_path = pathlib.Path(__package__)
    relative_path = pathlib.Path(DriverConfig.bin_dir + browser.bin_path +
                                 DriverConfig.suffixes[os.name])
    path = (base_path / relative_path).resolve()

    if (not os.path.exists(path)):
        message = 'ブラウザのドライバが存在しません.ドライバをダウンロードしてください. \nダウンロードURL=> ' + browser.download_url + \
            '\n実行ファイル ' + path.name + ' を \n' + \
            'ディレクトリ ' + str(path) + ' に配置してください.'
        raise EnvironmentError(message)
    return path
