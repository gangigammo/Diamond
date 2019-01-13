"""
カテゴリのモデル
"""
from django.db.models import Model, CharField, BooleanField
from .user import User


class Category(Model):
    """
    カテゴリの抽象クラスです

    Attributes
    ----------
    name : CharField
        カテゴリ名
    isIncome : BooleanField
        収入なら True
        支出なら False
    writer : User
        カテゴリの作成者
    """

    # Fields

    name = CharField(max_length=128)
    isIncome = BooleanField()
    writer = CharField(max_length=128)

    # public methods

    def __init__(self, name: str, writer: User, *args, **kwargs):
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
        super().__init__(*args, **kwargs)
        self._writer = writer
        self.update(name=name)

    def __str__(self):
        return self.name

    def update(self, **kwargs):
        """
        カテゴリの内容を変更します
        必ず名前付き引数で指定してください
        引数が省略された項目は無視されます

        Parameters
        ----------
        name : str
            新しいカテゴリ名
        """
        keys = kwargs.keys()
        if "name" in keys:
            self.name = kwargs.get("name")


class IncomeCategory(Category):
    """
    収入カテゴリのモデルです

    Attributes
    ----------
    name : CharField
        カテゴリ名
    isIncome : bool
        [読み取り専用]
        常にTrueを返します
    writer : User
        [読み取り専用]
        カテゴリの作成者
    """
    # accessors

    # Override Method
    @property
    def isIncome(self) -> bool:
        """
        常にTrueを返します
        """
        return True


class ExpenseCategory(Category):
    """
    支出カテゴリのモデルです

    Attributes
    ----------
    name : CharField
        カテゴリ名
    isIncome : bool
        [読み取り専用]
        常にFalseを返します
    writer : User
        [読み取り専用]
        カテゴリの作成者
    """
    # accessors

    # Override Method
    @property
    def isIncome(self) -> bool:
        """
        常にFalseを返します
        """
        return False
