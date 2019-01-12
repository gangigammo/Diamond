"""
	収支のモデル
"""
from django.db import models


class Balance(models.Model):
    description = models.CharField(max_length=128)
    amount = models.PositiveIntegerField()
    date = models.DateField()
    isIncome = models.BooleanField()
    categoryName = models.CharField(max_length=128)
    writer = models.CharField(max_length=128)
