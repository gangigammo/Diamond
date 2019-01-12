"""
収支のモデル
"""
from django.db.models import Model
from django.db.models import CharField, PositiveIntegerField, DateField, BooleanField
from django.db.models import ForeignKey
from django.db.models import CASCADE, SET_NULL
from .user import User
from .category import Category


class Balance(Model):
    """
    収支のモデルです

    Attributes
    ----------
    description : CharField
        内容
    amount : PositiveIntegerField
        金額
    date : DateField
        作成時刻
    writer : User
        # TODO [読み取り専用]
        この収支の作成者
    category : Category
        この収支が所属するカテゴリ
    categoryName : CharField
        # TODO [読み取り専用]
        category.nameと同じ
    """

    # public fields

    description = CharField(max_length=128)
    amount = PositiveIntegerField()
    isIncome = BooleanField()   # TODO Income, Expenseにクラスで分ける
    date = DateField()  # TODO
    # もとのカテゴリ削除時 -> __category=nullとなる (SET_NULL)
    category = ForeignKey(Category, null=True, on_delete=SET_NULL)
    # もとのユーザ削除時 -> この収支も一緒に削除される (CASCADE)
    writer = ForeignKey(User, on_delete=CASCADE)  # TODO アクセス制御
