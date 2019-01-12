"""
収支のモデル
"""
from django.db.models import Model
from django.db.models import CharField, PositiveIntegerField, DateField, BooleanField
from django.db.models import ForeignKey
from django.db.models import CASCADE, SET_NULL


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
    isIncome : BooleanField
        収入は true
        支出は false
    """
    description = CharField(max_length=128)
    amount = PositiveIntegerField()
    date = DateField()
    isIncome = BooleanField()
    categoryName = CharField(max_length=128)
    writer = CharField(max_length=128)

    # private fields

    # 所属するカテゴリ
    # もとのカテゴリ削除時 -> __category=nullとなる (SET_NULL)
    __category = ForeignKey("Category", on_delete=SET_NULL)

    # 作成者ユーザ
    # もとのユーザ削除時 -> この収支も一緒に削除される (CASCADE)
    __writer = ForeignKey("User", on_delete=CASCADE)
