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
        [読み取り専用]
        この収支の作成者
    date : DateField
        収支の日付
    category : Category
        この収支が所属するカテゴリ
    amount : int
        金額 (絶対値)
    value : IntegerField
        金額 (収入が正, 支出が負の値)
    value_signed : str
        [読み取り専用]
        金額に符号を付けた文字列
    isIncome : bool
        [読み取り専用]
        収入なら True
        支出なら False
    categoryName : CharField
        [読み取り専用]
        category.nameと同じ
    """

    # public fields

    description = CharField(max_length=128)
    date = DateField()  # TODO
    # もとのカテゴリ削除時 -> __category=nullとなる (SET_NULL)
    category = ForeignKey(Category, null=True, on_delete=SET_NULL)
    _value = IntegerField()

    # private fields

    # もとのユーザ削除時 -> この収支も一緒に削除される (CASCADE)
    _writer = ForeignKey(User, on_delete=CASCADE)

    # accesors

    @property
    def writer(self) -> CharField:
        return self._writer

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
    def value(self) -> IntegerField:
        return self._value

    @value.setter
    def value(self, value):  # Abstract Method
        raise NotImplementedError("抽象メソッドを呼びました")

    @property
    def value_signed(self) -> str:  # Abstract Method
        raise NotImplementedError("抽象メソッドを呼びました")

    @property
    def isIncome(self) -> bool:  # Abstract Method
        raise NotImplementedError("抽象メソッドを呼びました")

    @property
    def categoryName(self) -> CharField:
        return self.category.name

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
        self._writer = writer
        if amount is not None:
            self.amount = amount
        elif value is not None:
            self.value = value
        else:
            TypeError("amount, valueのどちらも指定されていません")
        self.update(
            description=description,
            date=date,
            category=category
        )

    def __str__(self):
        return self.description

    def update(self, **kwargs):
        """
        収支の内容を変更します
        必ず名前付き引数で指定してください
        引数が省略された項目は無視されます

        Parameters
        ----------
        description : str
            内容
        date: DateField
            収支の日付
        category: Category or None
            属するカテゴリ
            Noneはカテゴリなしを表します
        amount : int
            金額 (絶対値)
            入力する場合、valueは省略
        value : int
            金額 (収入が正, 支出が負の値)
            入力する場合、amountは省略
        """
        keys = kwargs.keys()
        if "description" in keys:
            self.description = kwargs.get("description")
        if "date" in keys:
            self.date = kwargs.get("date")
        if "category" in keys:
            self.category = kwargs.get("category")
        if "amount" in keys:
            self.amount = kwargs.get("amount")
        elif "value" in keys:
            self.value = kwargs.get("value")


class Income(Balance):
    """
    収入のモデルです
    valueとamountは連動します

    Attributes
    ----------
    description : CharField
        内容
    writer : User
        [読み取り専用]
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
        常にTrueを返します
    value_signed : str
        [読み取り専用]
        金額に符号を付けた文字列
    categoryName : CharField
        [読み取り専用]
        category.nameと同じ
    """
    # accessors

    # Override Method
    @amount.setter
    def amount(self, amount: int):
        """
        収支の金額を、絶対値で入力します
        """
        if amount < 0:
            raise ValueError("amountに負の値が入力されました")
        self.value = amount

    # Override Method
    @value.setter
    def value(self, value):
        if value < 0:
            raise ValueError("収入に負の値が入力されました")
        self._value = value

    # Override Method
    @property
    def value_signed(self) -> str:
        return "+" + str(self.value)

    # Override Method
    @property
    def isIncome(self) -> bool:
        return True


class Expense(Balance):
    """
    支出のモデルです
    valueとamountは連動します

    Attributes
    ----------
    description : CharField
        内容
    writer : User
        [読み取り専用]
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
        常にFalseを返します
    value_signed : str
        [読み取り専用]
        金額に符号を付けた文字列
    categoryName : CharField
        [読み取り専用]
        category.nameと同じ
    """

    # Override Method
    @amount.setter
    def amount(self, amount: int):
        """
        収支の金額を、絶対値で入力します
        """
        if amount < 0:
            raise ValueError("amountに負の値が入力されました")
        self.value = -amount

    # Override Method
    @value.setter
    def value(self, value):
        if value > 0:
            raise ValueError("支出に正の値が入力されました")
        self._value = value

    # Override Method
    @property
    def value_signed(self) -> str:
        return str(self.value)

    # Override Method
    @property
    def isIncome(self) -> bool:
        return False
