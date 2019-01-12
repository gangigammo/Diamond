"""
カテゴリのモデル
"""
from django.db.models import Model, CharField, BooleanField


class Category(Model):
    categoryName = CharField(max_length=128)
    balance = BooleanField()  # if income true, else false
    writer = CharField(max_length=128)
