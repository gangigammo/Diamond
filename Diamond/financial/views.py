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
    if request.method == 'POST':
        if 'Category' in request.POST:
            categoryName = request.POST["Category"]
            balances = Balance.objects.filter(categoryName=categoryName)
        else:
            balances = Balance.objects.all()
    else:
        balances = Balance.objects.all()
    incomes = []
    expences = []
    categories = Category.objects.all()
    incomeCategories = Category.objects.filter(balance = True)
    expenseCategories = Category.objects.filter(balance = False)
    categories = categories.values('categoryName').order_by('categoryName').distinct()
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

                  {"incomes":incomes, "expences":expences, "sumIncomes":sumIncomes, "sumExpences":sumExpences, "gain":gain,
                   "incomeCategories":incomeCategories, "expenseCategories":expenseCategories, "Category":categories})

def income(request):
    inputIncomeStr = request.POST["income"]
    description = request.POST["incomeDescription"]
    if inputIncomeStr.isdecimal() and description != "": #入力が数字の時
        inputIncome = int(inputIncomeStr)
        categoryName = request.POST["incomeCategory"]
        income = Balance(description=description, amount=inputIncome, isIncome=True, date=datetime.date.today(),
                     categoryName=categoryName)
        income.save()
        return render(request, "income.html")
    else: #入力が数字でない時のエラー
        if not inputIncomeStr.isdecimal():
            return viewError(request, "incomeError", "notDecimalError")
        else:
            return viewError(request, "incomeError", "contentBlankError")



def expence(request):
    inputExpenceStr = request.POST["expence"]
    description = request.POST["expenceDescription"]
    if inputExpenceStr.isdecimal() and description != "":
        inputExpence = int(inputExpenceStr)
        categoryName = request.POST["expenseCategory"]
        expence = Balance(description=description, amount=inputExpence, isIncome=False, date=datetime.date.today(),
                      categoryName=categoryName)
        expence.save()
        return render(request, "expence.html")
    else: #入力エラーの時
        if not inputExpenceStr.isdecimal():
            return viewError(request, "expenseError", "notDecimalError")
        else:
            return viewError(request, "expenseError", "contentBlankError")


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
    inputCategory = request.POST["registrationCategory"]
    categoryType = request.POST["categoryType"]
    if inputCategory == "":
        return viewError(request, "categorySubscribeError", "blank")
    if categoryType == "income":
        if len(IncomeCategory.objects.filter(categoryName=inputCategory)) == 0:
            newcategory = IncomeCategory(categoryName=inputCategory)
            newcategory.save()
        else:
            return viewError(request, "categorySubscribeError", "duplication")
    else:
        if len(ExpenseCategory.objects.filter(categoryName=inputCategory)) == 0:
            newcategory = ExpenseCategory(categoryName=inputCategory)
            newcategory.save()
        else:
            return viewError(request, "categorySubscribeError", "duplication")
    return render(request, "category.html")

def viewError(request,errorName,errorType):
    balances = Balance.objects.all()
    incomes = []
    expences = []
    categories = Category.objects.all()
    incomeCategories = Category.objects.filter(balance=True)
    expenseCategories = Category.objects.filter(balance=False)

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
        return render(request, "view.html",{"categorySubscribeError":"blank",
                                            "incomes": incomes, "expences": expences, "sumIncomes":sumIncomes, "sumExpences":sumExpences, "gain":gain,
                                            "incomeCategories": incomeCategories, "expenseCategories": expenseCategories
                                            })
    if categoryType == "income":
        if len(Category.objects.filter(categoryName=inputCategory, balance = True)) == 0:
            newcategory = Category(categoryName=inputCategory, balance = True)
            newcategory.save()
        else:
            return render(request, "view.html", {"categorySubscribeError": "duplication", "incomes": incomes, "expences": expences, "sumIncomes":sumIncomes, "sumExpences":sumExpences, "gain":gain,
                                            "incomeCategories": incomeCategories, "expenseCategories": expenseCategories})
    else:
        if len(Category.objects.filter(categoryName=inputCategory, balance = False)) == 0:
            newcategory = Category(categoryName=inputCategory, balance = False)
            newcategory.save()
        else:
            return render(request, "view.html", {"categorySubscribeError": "duplication", "incomes": incomes, "expences": expences, "sumIncomes":sumIncomes, "sumExpences":sumExpences, "gain":gain,
                                            "incomeCategories": incomeCategories, "expenseCategories": expenseCategories})
    return render(request, "category.html")

