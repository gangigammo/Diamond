"""
カテゴリのモデル
"""
from django.db.models import Model, CharField, BooleanField


class Category(Model):
    """
    カテゴリのモデルです

    Attributes
    ----------
    categoryName : CharField
        カテゴリ名
    balance : BooleanField
        収入は true
        支出は false
    writer : CharField
        カテゴリの作成者
    """
    categoryName = CharField(max_length=128)
    balance = BooleanField()  # if income true, else false
    writer = CharField(max_length=128)
