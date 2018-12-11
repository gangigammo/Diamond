from django.test import TestCase
from selenium import webdriver
import itertools

from .lib.driver import Browsers
from .lib.driver.browser import Browser
from .lib.driver import DriverFactory
from .lib.signin import *
from .lib.driver import driver_util


# 色々なユーザー名・パスワードでログイン可能かのテスト

class Test1(TestCase):
    def test_main(self):

        # (ユーザー名・パスワード) の列挙
        users = [("username", "password"),
                 ("YjSnpi114514", "mazuuchi"),
                 ("1919", "810364364")]

        # webdriver を作成
        driver = DriverFactory.new(Browsers.Chrome)
        driver.click_url("delete")
        driver.back()

        for user, password in users:
            print('[Case]\nuser : ' + user + '\npass:' + password)
            signup(driver, user, password)
            print('signup OK')
            signin(driver, user, password)
            driver.click_url("view")
            print('signin OK')
            signout(driver, user, password)
            print('signout OK')
            signin(driver, user, password + 'wrong')
            if (driver.exists("view")):
                raise AssertionError('間違ったパスワードでログインできてしまいました.')
            print('password authentication OK')

        # 閉じる
        driver.close()
        driver.quit()
        del driver
