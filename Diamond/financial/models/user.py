"""
ユーザーのモデル
"""
from django.db.models import Model, CharField


class User(Model):
    """
    ユーザーのモデルです

    Attributes
    ----------
    name : CharField
        # TODO [読み取り専用]
        ユーザー名
    password : CharField
        # TODO [書き込み専用]
        パスワード
    """

    # private field

    _name = CharField(max_length=128)
    _password = CharField(max_length=128)  # TODO 平文にしない　

    # TODO acceser

    # TODO initializer

    # TODO __str__

    # TODO password auth

    # TODO update password
