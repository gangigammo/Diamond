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

    Fields
    ------
    description : CharField
        内容
    writer : User
        この収支の作成者
    date : DateField
        収支の日付
    category : Category or None
        この収支が所属するカテゴリ
        カテゴリに属さない場合はNone
    value : IntegerField
        金額 (収入が正, 支出が負の値)
    isIncome : BooleanField
        収入なら True
        支出なら False

    Properties (Read Only)
    ----------------------
    amount : int
        金額 (絶対値)
    value_signed : str
        金額に符号を付けた文字列
    categoryName : CharField or None
        category.nameと同じ
        属するカテゴリが無ければNone
    """

    # Fields

    description = CharField(max_length=128)
    # もとのユーザ削除時 -> この収支も一緒に削除される (CASCADE)
    writer = ForeignKey(User, on_delete=CASCADE)
    date = DateField()  # TODO
    # もとのカテゴリ削除時 -> __category=nullとなる (SET_NULL)
    category = ForeignKey(Category, null=True, on_delete=SET_NULL)
    value = IntegerField()
    isIncome = BooleanField()

    # properties

    @property
    def amount(self) -> int:
        return abs(self.value)

    @property
    def value_signed(self) -> str:
        sign = "+" if self.isIncome else "-"
        return sign + str(self.amount)

    @property
    def categoryName(self) -> CharField:
        c = self.category
        return c and c.name

    # public methods

    def __str__(self):
        return self.description
