from django.shortcuts import render
from financial.models import *


def start(request):
    # TODO テスト用にトップページを返している
    return render(request, "home.html", {"name": request.session.get("name")})
