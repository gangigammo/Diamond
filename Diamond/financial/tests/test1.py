from django.test import TestCase
from selenium import webdriver
import itertools

from .lib.driver import Browsers
from .lib.driver.browser import Browser
from .lib.driver import DriverFactory
from .lib.signup import *
from . import cases


class Test1(TestCase):
    def test_main(self):
        # webdriver を作成
        ui = DriverFactory.new(Browsers.Chrome)
        # webdriver を操作
        signup(ui)
        # 閉じる
        del ui
