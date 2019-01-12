"""
カテゴリのモデル
"""
from django.db.models import Model, CharField, BooleanField
from .user import User


class Category(Model):
    """
    カテゴリの抽象クラスです
    具象クラス:
        - IncomeCategory
        - ExpenseCategory

    Attributes
    ----------
    name : CharField
        カテゴリ名
    isIncome : bool
        [読み取り専用]
        収入なら True
        支出なら False
    writer : User
        [読み取り専用]
        カテゴリの作成者
    """

    # public field

    name = CharField(max_length=128)

    # private fields

    _writer = CharField(max_length=128)

    # accessors

    @property
    def isIncome(self) -> bool:  # 抽象クラス
        """
        このインスタンスが収入であるか支出であるかを返します

        Return
        ------
        isincome : bool
            収入なら True
            支出なら False
        """
        raise NotImplementedError

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

    def update(self, name=None):
        """
        カテゴリの内容を変更します
        引数が省略されるかNoneである項目は無視されます

        Parameters
        ----------
        name : str or None
            新しいカテゴリ名
        """
        if name:
            self.name = name


class IncomeCategory(Category):
    """
    収入のモデルです

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
    支出のモデルです

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
