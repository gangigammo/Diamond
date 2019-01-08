from django.shortcuts import render
from financial.models import *


def start(request, balance_id):
    # TODO テスト用ページを返している
    return render(request, "balance/delete.html", {"id": balance_id})
