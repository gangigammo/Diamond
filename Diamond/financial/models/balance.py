"""
収支のモデル
"""
from django.db.models import Model, CharField, PositiveIntegerField, DateField, BooleanField


class Balance(Model):
    """
    収支のモデルです

    Attributes
    ----------
    description : CharField
    amount : PositiveIntegerField
    date : DateField
    isIncome : BooleanField
    """
    description = CharField(max_length=128)
    amount = PositiveIntegerField()
    date = DateField()
    isIncome = BooleanField()
    categoryName = CharField(max_length=128)
    writer = CharField(max_length=128)
