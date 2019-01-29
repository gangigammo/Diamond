"""Diamond URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

import financial.views as financial_view
from financial.view import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', financial_view.home),
    path('view/', financial_view.view),
    path('income/', financial_view.income),
    path('expence/', financial_view.expence),
    path('signin/', financial_view.signin),
    path('signup/', financial_view.signup),
    path('signinconfirm/', financial_view.signinconfirm),
    path('signupconfirm/', financial_view.signupconfirm),
    path('signout/', financial_view.signout),
    path('category/', financial_view.category),
    path('search/', financial_view.view),
    path('export/', financial_view.export),
    path('passwordchange/', financial_view.passwordchange),
    path('passwordchangeconfirm/', financial_view.passwordchangeconfirm),
    path('unregister/', financial_view.unregister),
    path('unregisterconfirm/', financial_view.unregisterconfirm),

    # 収支エントリの変更
    path('balanceedit/', balanceEdit.main),
    path('balanceedit/apply/', balanceEdit.apply)
]
