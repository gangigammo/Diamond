from django.shortcuts import render
from financial.models import Balance
from financial.view.util.balances import Balances


def start(request, balance_id):
    # TODO テスト用ページを返している
    balance = Balances.getById(balance_id)
    return render(request, "balance/delete.html", {"balance": balance})
