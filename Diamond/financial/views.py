from django.shortcuts import render

from financial.models import *
# Create your views here.

def home(request):
    return render(request, "home.html")

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
    inputIncome = int(inputIncomeStr)
    description = request.POST["incomeDescription"]
    categoryName = request.POST["incomeCategory"]
    income = Income(description=description, amount=inputIncome, categoryName=categoryName)
    income.save()
    return render(request, "income.html")

def expence(request):
    inputExpenceStr = request.POST["expence"]
    inputExpence = int(inputExpenceStr)
    description = request.POST["expenceDescription"]
    categoryName = request.POST["expenseCategory"]
    expence = Expense(description=description, amount=inputExpence, categoryName=categoryName)
    expence.save()
    return render(request, "expence.html")

def delete(request):
    incomes = Income.objects.all()
    expences = Expense.objects.all()
    incomeCategories = IncomeCategory.objects.all()
    expenseCategories = ExpenseCategory.objects.all()
    incomes.delete()
    expences.delete()
    incomeCategories.delete()
    expenseCategories.delete()
    return render(request, "delete.html")

def category(request):#カテゴリー登録関数
    incomes = Income.objects.all()
    expences = Expense.objects.all()
    incomeCategories = IncomeCategory.objects.all()
    expenseCategories = ExpenseCategory.objects.all()

    inputCategory = request.POST["registrationCategory"]
    categoryType = request.POST["categoryType"]
    if inputCategory == "":#入力が空白の時にエラー処理（URLがviewからcategoryに変更されてしまうので修正案件）
        return render(request, "view.html",{"categorySubscribeError":"blank",
                                            "incomes": incomes, "expences": expences,
                                            "incomeCategories": incomeCategories, "expenseCategories": expenseCategories
                                            })
    if categoryType == "income":
        if len(IncomeCategory.objects.filter(categoryName=inputCategory)) == 0:
            newcategory = IncomeCategory(categoryName=inputCategory)
            newcategory.save()
        else:#入力が重複した時のエラー処理（URLがviewからcategoryに変更されてしまうので修正案件）
            return render(request, "view.html", {"categorySubscribeError": "duplication", "incomes": incomes, "expences": expences,
                                            "incomeCategories": incomeCategories, "expenseCategories": expenseCategories})
    else:
        if len(ExpenseCategory.objects.filter(categoryName=inputCategory)) == 0:
            newcategory = ExpenseCategory(categoryName=inputCategory)
            newcategory.save()
        else:#入力が重複した時のエラー処理（URLがviewからcategoryに変更されてしまうので修正案件）
            return render(request, "view.html", {"categorySubscribeError": "duplication", "incomes": incomes, "expences": expences,
                                            "incomeCategories": incomeCategories, "expenseCategories": expenseCategories})
    return render(request, "category.html")
