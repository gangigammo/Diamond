from django.test import TestCase
from selenium import webdriver

from .lib.browsers import Browsers
from .lib.driver import Driver


class Test1(TestCase):
    def test_main(self):
        # webdriver を作成
        ui = Driver(Browsers.Chrome)
        # webdriver を操作

        # 閉じる
        ui.close()
        ui.quit()
