from django.test import TestCase
from selenium import webdriver

from .lib import diamond_ui


class Test1(TestCase):
    def test_main(self):
        # webdriver を作成
        ui = diamond_ui.new()
        # webdriver を操作

        # 閉じる
        ui.close()
        ui.quit()
