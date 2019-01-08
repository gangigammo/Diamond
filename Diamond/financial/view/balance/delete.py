from django.shortcuts import render
from financial.models import Balance
from financial.view.util.balances import Balances


template = "balance/delete.html"


def start(request, balance_id):
    # TODO テスト用ページを返している
    balance = Balances.getById(balance_id)
    message = not balance and "対象が存在しません"
    return render(request, template, {"balance": balance, "message": message})
