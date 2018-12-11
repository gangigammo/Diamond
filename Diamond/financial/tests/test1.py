from django.test import TestCase
from selenium import webdriver
import itertools

from .lib.browsers import Browsers
from .lib.driver import Driver
from . import cases


class Test1(TestCase):
    def test_main(self):
        # webdriver を作成
        ui = Driver(Browsers.Chrome)
        # webdriver を操作
        map(print, cases.users)

        # 閉じる
        del ui
