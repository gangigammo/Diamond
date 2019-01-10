from django.shortcuts import render
from financial.models import Balance
from financial.view.util.balances import Balances
from financial.views import view

template = "balance/delete.html"


def start(request, balance_id):
    balance = Balances.getById(balance_id)
    message = balance and "削除してよろしいですか？"
    message = message or "対象が存在しません"
    return render(request, template, {"balance": balance, "message": message})


def confirm(request, balance_id):
    balance = Balances.getById(balance_id)
    # TODO balanceの所有者以外が勝手に削除しないようにする
    balance and balance.delete()
    return view(request)
