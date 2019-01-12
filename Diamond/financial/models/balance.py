"""
収支のモデル
"""
from django.db.models import Model
from django.db.models import CharField, PositiveIntegerField, DateField, BooleanField


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
