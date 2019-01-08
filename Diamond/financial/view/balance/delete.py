from django.shortcuts import render
from financial.models import Balance


def start(request, balance_id):
    # TODO テスト用ページを返している
    balances = Balance.objects.filter(id=balance_id)
    for balance in balances:    # TODO コレクションからの取り出し
        return render(request, "balance/delete.html", {"balance": balance})
