"""
Balanceのふるまいのテスト
"""
from django.test import TestCase
from .checker import *

from financial.models import User
from financial.models import Balance, Income, Expense
from financial.models.objects import Balances, Incomes, Expenses
import datetime


class BalanceTest(TestCase):
    name = "watashi"
    password = "unkoman"
    user = User(name=name, password=password)

    desc = "hogedesc"
    amount = 114514
    date = datetime.date.today()
    income = Income(description=desc, writer=user, value=amount, date=date)
    expense = Expense(description=desc, writer=user, value=-amount, date=date)

    checkBalance(one=income, description=desc,
                 writer=user, value=amount, amount=amount, date=date)
    checkBalance(one=expense, description=desc,
                 writer=user, value=-amount, amount=amount, date=date)

    if income.value < 0:
        AssertionError("incomeの値が負です")
    if expense.value > 0:
        AssertionError("expenseの値が正です")

    try:
        income.save()
        expense.save()
    except Exception as ex:
        print("収支をデータベースに保存できませんでした")
        raise AssertionError(ex)
    print("Expenseモデルのテスト終了")


class BalancesTest(TestCase):
    raise NotImplementedError
    name = "watashi"
    password = "unkoman"
    user = User(name=name, password=password)

    desc = "hogedesc"
    amount = 114514
    date = datetime.date.today()
    income = Income(description=desc, writer=user, value=amount, date=date)
    expense = Expense(description=desc, writer=user, value=-amount, date=date)

    checkBalance(one=income, description=desc,
                 writer=user, value=amount, amount=amount, date=date)
    checkBalance(one=expense, description=desc,
                 writer=user, value=-amount, amount=amount, date=date)

    income.save()
    expense.save()

    balances = Balances.get()
    if not len(balances) == 2:
        raise AssertionError("データベースに保存されている個数が異常です")

    incomes = Incomes.get()
    expenses = Expenses.get()
    if not (len(incomes) == 1 and len(expenses) == 1):
        raise AssertionError("データベースに保存されている収支別の個数が異常です")

    if not compareBalance(income, incomes.first()):
        raise AssertionError("DBから取り出したincomeが異なります")
    if not compareBalance(expense, expenses.first()):
        raise AssertionError("DBから取り出したexpenseが異なります")
