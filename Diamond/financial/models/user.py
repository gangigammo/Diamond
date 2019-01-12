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
        ユーザー名
    password : CharField
        パスワード
    """
    name = CharField(max_length=128)
    password = CharField(max_length=128)
