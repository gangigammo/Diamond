from django.test import TestCase

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.common.exceptions import WebDriverException
import os
import pathlib

from .browsers import Browser

# ドライバーの設定


class DriverConfig():
    # ドライバー実行ファイルがあるパスを指定
    dir_path = '../Diamond/browsers/'
    # OSによって異なる実行ファイルの拡張子
    suffixes = {'nt': '.exe', 'posix': ''}


# ブラウザのドライバー

class Driver(WebDriver):
    def __init__(self, browser: Browser):
        path = DriverConfig.dir_path + browser.filename + \
            DriverConfig.suffixes[os.name]

        abs_path = pathlib.Path(path).resolve()

        if (os.path.exists(abs_path)):
            try:
                # ドライバーを返す
                self = browser.factory_method(str(abs_path))

            except WebDriverException:
                message = 'ブラウザ ' + browser.name + ' はインストールされていません.'
                raise EnvironmentError(message)
        else:
            message = 'ブラウザのドライバ ' + \
                str(abs_path) + ' が存在しません.' + \
                '\n ' + abs_path.name + ' のダウンロード: ' + browser.download_url
