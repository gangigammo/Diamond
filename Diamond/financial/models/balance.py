"""
収支のモデル
"""
from django.db.models import Model
from django.db.models import CharField, IntegerField, DateField, BooleanField
from django.db.models import ForeignKey
from django.db.models import CASCADE, SET_NULL
from .user import User
from .category import Category


class Balance(Model):
    """
    収支の抽象クラスです
    valueとamountは連動します

    具象クラス:
        - Income
        - Expense

    Attributes
    ----------
    description : CharField
        内容
    writer : User
        # TODO [読み取り専用]
        この収支の作成者
    date : DateField
        収支の日付
    category : Category
        この収支が所属するカテゴリ
    amount : int
        金額 (絶対値)
    value : IntegerField
        金額 (収入が正, 支出が負の値)
    isIncome : bool
        [読み取り専用]
        収入なら True
        支出なら False
    categoryName : CharField
        # TODO [読み取り専用]
        category.nameと同じ
    """

    # public fields

    description = CharField(max_length=128)
    date = DateField()  # TODO
    # もとのカテゴリ削除時 -> __category=nullとなる (SET_NULL)
    category = ForeignKey(Category, null=True, on_delete=SET_NULL)
    value = IntegerField()

    # private fields

    # 金額の内部表現 : 符号付きint
    # もとのユーザ削除時 -> この収支も一緒に削除される (CASCADE)
    _writer = ForeignKey(User, on_delete=CASCADE)

    # accesors

    @property
    def amount(self) -> int:
        return abs(self.value)

    @amount.setter
    def amount(self, amount: int):  # Abstract Method
        """
        収支の金額を、絶対値で入力します
        """
        raise NotImplementedError("抽象メソッドを呼びました")

    @property
    def isIncome(self):  # Abstract Method
        raise NotImplementedError("抽象メソッドを呼びました")

    # public methods

    def __init__(
        self,
        description: str,
        writer: User,
        date: DateField,
        category=None,
        amount=None, value=None,
        *args, **kwargs
    ):
        """
        Balanceを初期化します
        ただしBalanceは抽象クラスなので、
        インスタンスを生成するには具象クラスを実装してください

        なお、金額はamount, valueのどちらか一方に指定し、一方は省略してください

        Parameters
        ----------
        description : str
            内容
        writer : User
            作成者となるユーザー
        date: DateField
            収支の日付
        category: Category or None
            属するカテゴリ
        amount : int or None
            金額 (絶対値)
            入力する場合、valueは省略
        value : int or None
            金額 (収入が正, 支出が負の値)
            入力する場合、amountは省略
        """
        super().__init__(*args, **kwargs)
        self.description = description
        self._writer = writer
        self.date = date
        self.category = category
        if amount is not None:
            self.amount = amount
        elif value is not None:
            self.value = value
        else:
            TypeError("amount, valueのどちらも指定されていません")

    def __str__(self):
        return self.description

    def update(
        self,
        description: str,
        date: DateField,
        category=None,
        amount=None, value=None,
        *args, **kwargs
    ):
        """
        収支の内容を変更します
        引数が省略されるかNoneである項目は無視されます

        Parameters
        ----------
        description : str or None
            内容
        date: DateField or None
            収支の日付
        category: Category or None
            属するカテゴリ
        amount : int or None
            金額 (絶対値)
            入力する場合、valueは省略
        value : int or None
            金額 (収入が正, 支出が負の値)
            入力する場合、amountは省略
        """
        if not description is None:
            self.description = description
        if not date is None:
            self.date = date
        if not category is None:
            self.category = category
        if amount is not None:
            self.amount = amount
        elif value is not None:
            self.value = value

# TODO class Income
# TODO class Expense
