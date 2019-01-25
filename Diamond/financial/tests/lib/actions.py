
from selenium.webdriver.remote.webdriver import WebDriver

from .driver import driver_util
from .driver import DriverConfig


# 収入を追加する
def addIncome(self: WebDriver, amount: int, description: str, category=None):
    category = category or "選択なし"
    form_id = "incomeForm"
    select_name = "incomeCategory"
    input_dict = {"income": amount,
                  "incomeDescription": description,
                  }

    self.pushButton("income_btn")
    category and self.pushSelect(
        form_id=form_id, name=select_name, value=category)
    self.form_submit(form_id, input_dict)
    print("    added "+str(input_dict))
    self.click_url("view")


# 支出を追加する
def addExpense(self: WebDriver, amount: int, description: str, category=None):
    category = category or "選択なし"
    form_id = "expenceForm"
    select_name = "expenseCategory"
    input_dict = {"expence": amount,
                  "expenceDescription": description,
                  }

    self.pushButton("expense_btn")
    category and self.pushSelect(
        form_id=form_id, name=select_name, value=category)
    self.form_submit(form_id, input_dict)
    print("    added "+str(input_dict))
    self.click_url("view")


# カテゴリを追加する
def __addCategory(self: WebDriver, name: str, categoryType: str):
    form_id = "categoryForm"
    select_name = "categoryType"
    input_dict = {"registrationCategory": name}
    self.pushButton("category_btn")
    self.pushSelect(form_id=form_id, name=select_name, value=categoryType)
    self.form_submit(form_id, input_dict)
    print("    added "+str(input_dict))
    self.click_url("view")


def addIncomeCategory(self: WebDriver, name: str):
    self.__addCategory(name=name, categoryType="income")


def addExpenseCategory(self: WebDriver, name: str):
    self.__addCategory(name=name, categoryType="expense")


# メソッドをWebDriverに追加
def __setattr(method):
    setattr(WebDriver, method.__name__, method)


__setattr(addIncome)
__setattr(addExpense)
__setattr(__addCategory)
__setattr(addIncomeCategory)
__setattr(addExpenseCategory)
