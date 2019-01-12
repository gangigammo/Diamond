"""
カテゴリのモデル
"""
from django.db.models import Model, CharField, BooleanField
from .user import User


class Category(Model):
    """
    カテゴリの抽象クラスです
    具象クラス:
        - Income
        - Expense

    Attributes
    ----------
    name : CharField
        カテゴリ名
    isIncome : # TODO bool
        # TODO [読み取り専用]
        収入は true
        支出は false
    writer : User
        # [読み取り専用]
        カテゴリの作成者
    """

    # public field

    name = CharField(max_length=128)

    # private fields

    _writer = CharField(max_length=128)

    # accesers

    @property
    def writer(self) -> str:
        return self._writer

    # public methods

    def __init__(self, name: str, writer: User):
        """
        Categoryを初期化します
        ただしCategoryは抽象クラスなので、
        インスタンスを生成するには具象クラスを実装してください

        Parameters
        ----------
        name : str
            カテゴリ名
        writer : User
            作成者となるユーザー
        """
        super().__init__()

    def __str__(self):
        return self.name

    # TODO update name
