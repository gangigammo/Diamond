from django.shortcuts import render
from django.shortcuts import redirect
from financial.models import *

# Create your views here.

def home(request):
    return render(request, "home.html", {"name":request.session.get("name")})

def view(request):
    incomes = Income.objects.all()
    expences = Expense.objects.all()
    incomeCategories = IncomeCategory.objects.all()
    expenseCategories = ExpenseCategory.objects.all()
    sumIncomes = 0
    for income in incomes:
        sumIncomes = sumIncomes + income.amount
    sumExpences = 0
    for expence in expences:
        sumExpences = sumExpences + expence.amount
    gain = sumIncomes - sumExpences
    return render(request, "view.html",
                  {"incomes":incomes, "expences":expences, "sumIncomes":sumIncomes, "sumExpences":sumExpences, "gain":gain,
                   "incomeCategories":incomeCategories, "expenseCategories":expenseCategories})

def income(request):
    inputIncomeStr = request.POST["income"]
    description = request.POST["incomeDescription"]
    if inputIncomeStr.isdecimal() and description != "": #入力が数字の時
        inputIncome = int(inputIncomeStr)
        categoryName = request.POST["incomeCategory"]
        income = Income(description=description, amount=inputIncome, categoryName=categoryName)
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
        expence = Expense(description=description, amount=inputExpence, categoryName=categoryName)
        expence.save()
        return render(request, "expence.html")
    else: #入力エラーの時
        if not inputExpenceStr.isdecimal():
            return viewError(request, "expenseError", "notDecimalError")
        else:
            return viewError(request, "expenseError", "contentBlankError")


def delete(request):
    incomes = Income.objects.all()
    expences = Expense.objects.all()
    user = User.objects.all()
    incomeCategories = IncomeCategory.objects.all()
    expenseCategories = ExpenseCategory.objects.all()
    incomes.delete()
    expences.delete()
    user.delete()
    incomeCategories.delete()
    expenseCategories.delete()
    request.session.flush()
    return render(request, "delete.html")

def signin(request):
    return render(request, "signin.html",{"error":"none"})

def signup(request):
    return render(request, "signup.html",{"error":"none"})

def signinconfirm(request):
    name = request.POST["name"]
    password = request.POST["password"]
    if len(User.objects.filter(name=name)) != 0:
        if User.objects.filter(name=name)[0].password == password:
            request.session["name"] = name
            return render(request, "home.html", {"name":request.session.get("name")})
        else:
            return render(request, "signin.html", {"error":"password"})
    else:
        return render(request, "signin.html", {"error":"name"})

def signupconfirm(request):
    name = request.POST["name"]
    password = request.POST["password"]
    if len(User.objects.filter(name=name)) == 0:
        user = User(name = name, password = password)
        user.save()
        return render(request, "home.html")
    else:
        return render(request, "signup.html", {"error":"name"})

def signout(request):
    request.session.clear()
    return render(request, "home.html", {"name":request.session.get("name")})

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
    incomes = Income.objects.all()
    expences = Expense.objects.all()
    incomeCategories = IncomeCategory.objects.all()
    expenseCategories = ExpenseCategory.objects.all()
    sumIncomes = 0
    for income in incomes:
        sumIncomes = sumIncomes + income.amount
    sumExpences = 0
    for expence in expences:
        sumExpences = sumExpences + expence.amount
    gain = sumIncomes - sumExpences
    return render(request, "view.html",
                  {errorName: errorType, "incomes": incomes, "expences": expences,
                   "sumIncomes": sumIncomes, "sumExpences": sumExpences, "gain": gain,
                   "incomeCategories": incomeCategories, "expenseCategories": expenseCategories})

