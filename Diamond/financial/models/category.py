"""
	カテゴリのモデル
"""
from django.db import models


class Category(models.Model):
    categoryName = models.CharField(max_length=128)
    balance = models.BooleanField()  # if income true, else false
    writer = models.CharField(max_length=128)
