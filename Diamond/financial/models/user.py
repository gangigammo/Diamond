"""
ユーザーのモデル
"""
from django.db.models import Model, CharField


class User(Model):
    name = CharField(max_length=128)
    password = CharField(max_length=128)
