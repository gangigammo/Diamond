from django.test import TestCase
from selenium import webdriver
from financial.models import User, Balance, Category
from .lib.driver import Browsers
from .lib.driver import DriverFactory
from .lib.driver import driver_util
from .lib.sign import *
from .lib.actions import *
from functools import reduce
from operator import add
import copy

# 収支・カテゴリ追加機能のテスト

inCateNames = [
    "定期"
]
exCateNames = [
    "大きな買い物"
]

incomeDics = [
    {
        "amount": 10000,
        "description": "ゆきち"
    },
    {
        "amount": 1000,
        "description": "のぐちひでよ",
        "category": inCateNames[0]
    },
]

expenseDics = [
    {
        "amount": 160,
        "description": "お茶"
    },
    {
        "amount": 4000000,
        "description": "くるま",
        "category": exCateNames[0]
    },
]


class Test2(TestCase):
    def test_main(self):
        User.objects.all().delete()
        Balance.objects.all().delete()
        Category.objects.all().delete()

        # (ユーザー名・パスワード) の列挙
        users = [("username", "password"),
                 ("user2", "pass2")]

        # webdriver を作成
        try:
            driver = DriverFactory.new(Browsers.Chrome)
        except Exception as err:
            print(err)
            print("テストをスキップします")
            return

        for user, password in users:
            # view画面へ
            print('[Case]\nuser : ' + user + '\npass:' + password)
            signup(driver, user, password)
            signin(driver, user, password)
            driver.click_url("view")
            # 色々と追加
            for name in inCateNames:
                addIncomeCategory(driver, name)
                print("OK: 収入カテゴリ %s を追加" % str(name))
            for name in exCateNames:
                addExpenseCategory(driver, name)
                print("OK: 支出カテゴリ %s を追加" % str(name))
            for dic in incomeDics:
                addIncome(driver, **dic)
                print("OK: 収入 %s を追加" % str(dic))
            for dic in expenseDics:
                addExpense(driver, **dic)
                print("OK: 支出 %s を追加" % str(dic))
            # 簡易チェック
            __indics = copy.deepcopy(incomeDics)
            __exdics = copy.deepcopy(expenseDics)
            for dic in __indics:
                dic["amount"] = "+%d" % dic["amount"]
            for dic in __exdics:
                dic["amount"] = "-%d" % dic["amount"]
            dics = __indics + __exdics
            values = reduce(add, [list(dic.values()) for dic in dics])
            for value in values:
                if not driver.exists(str(value)):
                    raise AssertionError("NG: 値 %s が収支表にありません" % value)
            signout(driver, user, password)

        # 閉じる
        driver.close()
        driver.quit()
        del driver
