"""
金剛会計におけるModelの、データベースとのやり取りを担当するモジュール
"""

from django.db.models.query import QuerySet
from django.db.models import Model
from typing import Optional, TypeVar, Generic, Sequence


T = Sequence[Model]


class AppObjects():
    _T = T
    """
    金剛会計におけるModelの、データベースとのやり取りを担当するクラス

    このクラスの処理は、classmethodとして実装されています。(Javaでいうところのstatic method)
    インスタンスからではなく、クラスからメソッドを呼び出してください
    ex.> all = AppObjects.getAll()

    このクラスを直接使うのではなく、以下のサブクラスを利用することを想定しています
    Users
        ユーザー
    Balances
        収支
    Incomes
        収入
    Expenses
        支出
    Categories
        収支カテゴリ
    IncomeCategories
        収入カテゴリ
    ExpenseCategories
        支出カテゴリ

    Attributes
    ----------
    _T : type (subtype of django.db.models.Model)
        このクラスが扱うデータのモデルの型
    """

    @classmethod
    def getObjects(cls):
        return cls._T.objects

    @classmethod
    def get(cls, *args, **kwargs) -> QuerySet:
        """
        データベースから、条件に合致する項目を取得します
        Return a new QuerySet instance with the args ANDed to the database.

        Parameters
        ----------
        検索項目=値
            検索項目が値に合致するものを絞り込む
        検索項目__in=値リスト
            検索項目が値リスト内のどれかに合致するものを絞り込む

        Returns
        -------
        objects : QuerySet of Model
            検索結果のQuerySet
        """
        return cls.getObjects().filter(**kwargs)

    @classmethod
    def getFirst(cls, *args, **kwargs) -> Optional[T]:
        """
        データベースから、条件に合致する項目を1つ取得します
        なければNoneを返します
        Return the first object of a query or None if no match is found.

        Parameters
        ----------
        検索項目=値
            検索項目が値に合致するものを絞り込む
        検索項目__in=値リスト
            検索項目が値リスト内のどれかに合致するものを絞り込む

        Returns
        -------
        objects : Model or None
            検索結果のModel
        """
        return cls.get().first()
