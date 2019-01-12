"""
カテゴリのモデル
"""
from django.db.models import Model, CharField, BooleanField


class Category(Model):
    """
    カテゴリのモデルです

    Attributes
    ----------
    name : CharField
        カテゴリ名
    isIncome : # TODO bool
        # TODO [読み取り専用]
        収入は true
        支出は false
    writer : User
        # TODO [読み取り専用]
        カテゴリの作成者
    """

    # public field

    name = CharField(max_length=128)

    # TODO private field

    isIncome = BooleanField()  # if income true, else false
    writer = CharField(max_length=128)

    # TODO acceser

    # TODO initializer

    # TODO __str__

    # TODO update name
