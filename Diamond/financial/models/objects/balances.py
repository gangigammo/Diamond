"""
金剛会計における収支を、データベースとやり取りするモジュール
"""
from .appobjects import AppObjects
from typing import Sequence
from financial.models import Balance, Income, Expense


T = Sequence[Balance]


class Balances(AppObjects):
    _T = Balance  # Override
    """
    金剛会計における収支を、データベースとやり取りするクラス

    このクラスの処理は、classmethodとして実装されています。(Javaでいうところのstatic method)
    インスタンスからではなく、クラスからメソッドを呼び出してください
    ex.> allBalances = Balances.getAll()

    Attributes
    ----------
    _T : type
        financial.models.Balance
    """

    # Override Method
    @classmethod
    def getObjects(cls):
        return Incomes.getObjects() + Expenses.getObjects()


class Incomes(Balances):
    _T = Income  # Override
    """
    金剛会計における収入を、データベースとやり取りするクラス

    このクラスの処理は、classmethodとして実装されています。(Javaでいうところのstatic method)
    インスタンスからではなく、クラスからメソッドを呼び出してください
    ex.> allIncomes = Incomes.getAll()

    Attributes
    ----------
    _T : type
        financial.models.Income
    """
    # Override Method
    @classmethod
    def getObjects(cls):
        return cls._T.objects


class Expenses(Balances):
    _T = Expense  # Override
    """
    金剛会計における支出を、データベースとやり取りするクラス

    このクラスの処理は、classmethodとして実装されています。(Javaでいうところのstatic method)
    インスタンスからではなく、クラスからメソッドを呼び出してください
    ex.> allExpenses = Expenses.getAll()

    Attributes
    ----------
    _T : type
        financial.models.Expense
    """
    # Override Method
    @classmethod
    def getObjects(cls):
        return cls._T.objects
