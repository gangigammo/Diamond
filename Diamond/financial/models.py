from django.db import models

# Create your models here.
class Balance(models.Model):  # 収支のモデル
    description = models.CharField(max_length=128)
    amount = models.PositiveIntegerField()
    date = models.DateField()
    isIncome = models.BooleanField()
    categoryName = models.CharField(max_length=128)
    userName = models.CharField(max_length=128)
class User(models.Model): #ユーザーのモデル
    name = models.CharField(max_length=128)
    password = models.CharField(max_length=128)


class IncomeCategory(models.Model):
    categoryName = models.CharField(max_length=128)


class ExpenseCategory(models.Model):
    categoryName = models.CharField(max_length=128)