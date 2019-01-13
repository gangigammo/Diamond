"""
金剛会計における収支を、データベースとやり取りするモジュール
"""
from .appobjects import AppObjects
from typing import Sequence
from financial.models import Balance


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


class Incomes(Balances):
    """
    金剛会計における収入を、データベースとやり取りするクラス

    このクラスの処理は、classmethodとして実装されています。(Javaでいうところのstatic method)
    インスタンスからではなく、クラスからメソッドを呼び出してください
    ex.> allIncomes = Incomes.getAll()
    """
    # Override Method
    @classmethod
    def getObjects(cls):
        return cls._T.objects.filter(isIncome=True)


class Expenses(Balances):
    """
    金剛会計における支出を、データベースとやり取りするクラス

    このクラスの処理は、classmethodとして実装されています。(Javaでいうところのstatic method)
    インスタンスからではなく、クラスからメソッドを呼び出してください
    ex.> allExpenses = Expenses.getAll()
    """
    # Override Method
    @classmethod
    def getObjects(cls):
        return cls._T.objects.filter(isIncome=False)
