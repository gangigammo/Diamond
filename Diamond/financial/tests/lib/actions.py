
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


__inCategoryPrefix = "収入: "
__exCategoryPrefix = "支出: "


def __changeCategory(self: WebDriver, name_from: str, name_to: str, prefix: str):
    form_id = "categoryEditForm"
    select_name = "categoryID"
    value = prefix + name_from
    input_dict = {"categoryName": name_to}
    self.pushButton("category_edit_btn")
    self.pushSelectByText(form_id=form_id, name=select_name, text=value)
    self.form_input(form_id, input_dict)
    self.form_click(form_id, "change")
    print("    changed %s -> %s" % (value, name_to))


def changeIncomeCategory(self: WebDriver, name_from: str, name_to: str):
    self.__changeCategory(name_from, name_to, __inCategoryPrefix)


def changeExpenseCategory(self: WebDriver, name_from: str, name_to: str):
    self.__changeCategory(name_from, name_to, __exCategoryPrefix)


def __deleteCategory(self: WebDriver, name: str, prefix: str):
    form_id = "categoryEditForm"
    select_name = "categoryID"
    value = prefix + name
    self.pushButton("category_edit_btn")
    self.pushSelectByText(form_id=form_id, name=select_name, text=value)
    self.form_click(form_id, "delete")
    print("    deleted category %s" % value)


def deleteIncomeCategory(self: WebDriver, name: str):
    self.__deleteCategory(name, __inCategoryPrefix)


def deleteExpenseCategory(self: WebDriver, name: str):
    self.__deleteCategory(name, __exCategoryPrefix)


# メソッドをWebDriverに追加


def __setattr(method):
    setattr(WebDriver, method.__name__, method)


__setattr(addIncome)
__setattr(addExpense)
__setattr(__addCategory)
__setattr(addIncomeCategory)
__setattr(addExpenseCategory)
__setattr(__changeCategory)
__setattr(changeIncomeCategory)
__setattr(changeExpenseCategory)
__setattr(__deleteCategory)
__setattr(deleteIncomeCategory)
__setattr(deleteExpenseCategory)
