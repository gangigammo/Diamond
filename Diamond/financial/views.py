from django.shortcuts import render

from financial.models import *
# Create your views here.

def home(request):
    return render(request, "home.html")

def view(request):
    incomes = Income.objects.all()
    expences = Expense.objects.all()
    sumIncomes = 0
    for income in incomes:
        sumIncomes = sumIncomes + income.amount
    sumExpences = 0
    for expence in expences:
        sumExpences = sumExpences + expence.amount
    gain = sumIncomes - sumExpences
    return render(request, "view.html",{"incomes":incomes, "expences":expences, "sumIncomes":sumIncomes, "sumExpences":sumExpences, "gain":gain})

def income(request):
    inputIncomeStr = request.POST["income"]
    inputIncome = int(inputIncomeStr)
    description = request.POST["incomeDescription"]
    income = Income(description=description, amount=inputIncome)
    income.save()
    return render(request, "income.html")

def expence(request):
    inputExpenceStr = request.POST["expence"]
    inputExpence = int(inputExpenceStr)
    description = request.POST["expenceDescription"]
    expence = Expense(description=description, amount=inputExpence)
    expence.save()
    return render(request, "expence.html")

def delete(request):
    incomes = Income.objects.all()
    expences = Expense.objects.all()
    incomes.delete()
    expences.delete()
    return render(request, "delete.html")

def signin(request):
    return render(request, "signin.html")