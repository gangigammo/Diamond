"""
Balanceのふるまいのテスト
"""
from django.test import TestCase
from .checker import *

from financial.models import User
from financial.models import Balance
from financial.models.objects import Balances, Incomes, Expenses
import datetime


class BalanceTest(TestCase):
    name = "watashi"
    password = "unkoman"
    user = User(name=name, password=password)
    user.save()

    desc = "hogedesc"
    amount = 114514
    date = datetime.date.today()
    income = Balance(isIncome=True, description=desc,
                     writer=user, value=amount, date=date)
    expense = Balance(isIncome=False, description=desc,
                      writer=user, value=-amount, date=date)

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
    except Exception as ex:
        print("incomeをデータベースに保存できませんでした")
        raise AssertionError(ex)
    try:
        expense.save()
    except Exception as ex:
        print("expenseをデータベースに保存できませんでした")
        raise AssertionError(ex)

    print("Balanceモデルのテスト終了")


class BalancesTest(TestCase):
    Balance.objects.all().delete()

    name = "watashi"
    password = "unkoman"
    user = User(name=name, password=password)
    user.save()

    desc = "hogedesc"
    amount = 114514
    date = datetime.date.today()
    income = Balance(isIncome=True, description=desc,
                     writer=user, value=amount, date=date)
    expense = Balance(isIncome=False, description=desc,
                      writer=user, value=-amount, date=date)

    checkBalance(one=income, description=desc,
                 writer=user, value=amount, amount=amount, date=date)
    checkBalance(one=expense, description=desc,
                 writer=user, value=-amount, amount=amount, date=date)

    income.save()
    expense.save()

    firstincome = Incomes.getFirst()
    firstexpense = Expenses.getFirst()
    if firstincome is None or firstexpense is None:
        raise AssertionError("データベースから収支を取得できません")

    incomes = Incomes.get()
    expenses = Expenses.get()
    if incomes.count() != 1 or expenses.count() != 1:
        print("incomes .count=%d" % incomes.count())
        print("expenses.count=%d" % expenses.count())
        raise AssertionError("データベースに保存されている収支別の個数が異常です")

    try:
        balances = Balances.get()
    except Exception as ex:
        print("Balancesから収支を取得できません")
        raise AssertionError(ex)

    if not len(balances) == 2:
        raise AssertionError("データベースに保存されている個数が異常です")

    if not compareBalance(income, incomes.first()):
        raise AssertionError("DBから取り出したincomeが異なります")
    if not compareBalance(expense, expenses.first()):
        raise AssertionError("DBから取り出したexpenseが異なります")

    print("Balancesのテスト終了")
