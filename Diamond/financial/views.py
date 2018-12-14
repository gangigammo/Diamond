from django.shortcuts import render
from django.shortcuts import redirect
from financial.models import *

import datetime

# Create your views here.


def home(request):
    return render(request, "home.html", {"name": request.session.get("name")})


def view(request):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    balances = Balance.objects.all()
    incomes = []
    expences = []
    incomeCategories = IncomeCategory.objects.all()
    expenseCategories = ExpenseCategory.objects.all()
    sumIncomes = 0
    sumExpences = 0
    for balance in balances:
        if balance.isIncome:
            incomes += [balance]
            sumIncomes += balance.amount
        else:
            expences += [balance]
            sumExpences += balance.amount

    gain = sumIncomes - sumExpences

    #グラフの用意
    if len(incomes) > 0:
        label = []
        amount = []
        for income in incomes:
            if not income.categoryName in label:
                label += [income.categoryName]
                amount += [income.amount]
            else:
                index = label.index(income.categoryName)
                amount[index] += income.amount
        fig = plt.figure(1, figsize=(4, 4))
        ax = fig.add_subplot(111)
        ax.axis("equal")
        ax.pie(amount,  # データ
                    startangle=90,  # 円グラフ開始軸を指定
                    labels=label,  # ラベル
                    autopct="%1.1f%%",  # パーセント表示
                   # colors=colors,  # 色指定
                    counterclock=False,  # 逆時計回り
                    )
        plt.savefig('figure.png')
    return render(request, "view.html",
                  {"incomes": incomes, "expences": expences, "sumIncomes": sumIncomes, "sumExpences": sumExpences, "gain": gain,
                   "incomeCategories": incomeCategories, "expenseCategories": expenseCategories})


def income(request):
    inputIncomeStr = request.POST["income"]
    inputIncome = int(inputIncomeStr)
    description = request.POST["incomeDescription"]
    categoryName = request.POST["incomeCategory"]
    income = Balance(description=description, amount=inputIncome, isIncome=True, date=datetime.date.today(),
                     categoryName=categoryName)
    income.save()
    return render(request, "income.html")


def expence(request):
    inputExpenceStr = request.POST["expence"]
    inputExpence = int(inputExpenceStr)
    description = request.POST["expenceDescription"]
    categoryName = request.POST["expenseCategory"]
    expence = Balance(description=description, amount=inputExpence, isIncome=False, date=datetime.date.today(),
                      categoryName=categoryName)
    expence.save()
    return render(request, "expence.html")


def delete(request):
    balances = Balance.objects.all()
    user = User.objects.all()
    incomeCategories = IncomeCategory.objects.all()
    expenseCategories = ExpenseCategory.objects.all()
    balances.delete()
    user.delete()
    incomeCategories.delete()
    expenseCategories.delete()
    request.session.flush()
    return render(request, "delete.html")


def signin(request):
    return render(request, "signin.html", {"error": "none"})


def signup(request):
    return render(request, "signup.html", {"error": "none"})


def signinconfirm(request):
    name = request.POST["name"]
    password = request.POST["password"]

    if len(User.objects.filter(name=name)) != 0:
        if User.objects.filter(name=name)[0].password == password:
            request.session["name"] = name
            return render(request, "home.html", {"name": request.session.get("name")})
        else:
            return render(request, "signin.html", {"error": "password"})
    else:
        return render(request, "signin.html", {"error": "name"})


def signupconfirm(request):
    name = request.POST["name"]
    password = request.POST["password"]
    if len(User.objects.filter(name=name)) == 0:
        user = User(name=name, password=password)
        user.save()
        return render(request, "home.html")
    else:
        return render(request, "signup.html", {"error": "name"})


def signout(request):
    request.session.clear()
    return render(request, "home.html", {"name": request.session.get("name")})

def category(request):#カテゴリー登録関数
    balances = Balance.objects.all()
    incomes = []
    expences = []
    incomeCategories = IncomeCategory.objects.all()
    expenseCategories = ExpenseCategory.objects.all()
    sumIncomes = 0
    sumExpences = 0
    for balance in balances:
        if balance.isIncome:
            incomes += [balance]
            sumIncomes += balance.amount
        else:
            expences += [balance]
            sumExpences += balance.amount

    gain = sumIncomes - sumExpences
    inputCategory = request.POST["registrationCategory"]
    categoryType = request.POST["categoryType"]
    if inputCategory == "":
        return render(request, "view.html", {"categorySubscribeError": "blank",
                                             "incomes": incomes, "expences": expences, "sumIncomes": sumIncomes, "sumExpences": sumExpences, "gain": gain,
                                             "incomeCategories": incomeCategories, "expenseCategories": expenseCategories
                                             })
    if categoryType == "income":
        if len(IncomeCategory.objects.filter(categoryName=inputCategory)) == 0:
            newcategory = IncomeCategory(categoryName=inputCategory)
            newcategory.save()
        else:
            return render(request, "view.html", {"categorySubscribeError": "duplication", "incomes": incomes, "expences": expences, "sumIncomes": sumIncomes, "sumExpences": sumExpences, "gain": gain,
                                                 "incomeCategories": incomeCategories, "expenseCategories": expenseCategories})
    else:
        if len(ExpenseCategory.objects.filter(categoryName=inputCategory)) == 0:
            newcategory = ExpenseCategory(categoryName=inputCategory)
            newcategory.save()
        else:
            return render(request, "view.html", {"categorySubscribeError": "duplication", "incomes": incomes, "expences": expences, "sumIncomes": sumIncomes, "sumExpences": sumExpences, "gain": gain,
                                                 "incomeCategories": incomeCategories, "expenseCategories": expenseCategories})
    return render(request, "category.html")
