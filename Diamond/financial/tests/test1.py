from django.test import TestCase
from selenium import webdriver
from financial.models import User
from .lib.driver import Browsers
from .lib.driver import DriverFactory
from .lib.driver import driver_util
from .lib.sign import *


# 色々なユーザー名・パスワードでログイン可能かのテスト

class Test1(TestCase):
    def test_main(self):
        # テスト前にデータベースを削除
        User.objects.all().delete()
        print('テスト準備: Userデータベースを削除しました.')

        # (ユーザー名・パスワード) の列挙
        users = [("YjSnpi114514", "810364364")]

        # webdriver を作成
        try:
            driver = DriverFactory.new(Browsers.Chrome)
        except Exception as err:
            print(err)
            print("テストをスキップします")
            return

        for user, password in users:
            print('[Case]\nuser : ' + user + '\npass:' + password)
            signup(driver, user, password)
            print('OK: サインアップ完了画面の表示')
            signin(driver, user, password)
            driver.click_url("view")
            print('OK: ログイン')
            signout(driver, user, password)
            print('OK: ログアウト')
            signin(driver, user, password + 'wrong')
            if (driver.exists("view")):
                raise AssertionError('間違ったパスワードでログインできてしまいました.')
            print('OK: ログイン')

        # 閉じる
        driver.close()
        driver.quit()
        del driver
