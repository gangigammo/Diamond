"""
金剛会計における収支カテゴリを、データベースとやり取りするモジュール
"""
from .appobjects import AppObjects
from typing import Sequence
from financial.models import Category


T = Sequence[Category]


class Categories(AppObjects):
    _T = T  # Override
    """
    金剛会計における収支カテゴリを、データベースとやり取りするクラス

    ex.> all = Categories.getAll()

    Attributes
    ----------
    _T : type
        financial.models.Category
    """


class IncomeCategories(Categories):
    _T = T  # Override
    """
    金剛会計における収入カテゴリを、データベースとやり取りするクラス

    ex.> all = IncomeCategories.getAll()

    Attributes
    ----------
    _T : type
        financial.models.IncomeCategory
    """


class ExpenseCategories(Categories):
    _T = T  # Override
    """
    金剛会計における支出カテゴリを、データベースとやり取りするクラス

    ex.> all = ExpenseCategories.getAll()

    Attributes
    ----------
    _T : type
        financial.models.ExpenseCategory
    """
