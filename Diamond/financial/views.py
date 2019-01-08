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
    if request.method == 'POST':
        if 'Category' in request.POST:
            categoryName = request.POST["Category"]
            balances = Balance.objects.filter(categoryName=categoryName)
        else:
            balances = Balance.objects.all()
    else:
        balances = Balance.objects.all()
    username = request.session["name"]
    balances = Balance.objects.filter(userName=username)
    incomes = []
    expences = []
    categories = Category.objects.all()
    incomeCategories = Category.objects.filter(balance=True)
    expenseCategories = Category.objects.filter(balance=False)
    categories = categories.values(
        'categoryName').order_by('categoryName').distinct()
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

    # グラフの用意
    createIncomeCircle(request)
    createExpenceCircle(request)
    return render(request, "view.html",
                  {"user":username, "incomes":incomes, "expences":expences, "sumIncomes":sumIncomes, "sumExpences":sumExpences, "gain":gain,
                   "incomeCategories":incomeCategories, "expenseCategories":expenseCategories,
                   "incomeFileName":getFileName(request, 'circle_income'),
                   "expenceFileName":getFileName(request, 'circle_expence')})


def getFileName(request, basename):
    # 更新日を付与した画像のファイル名を返す
    import os
    import glob
    username = request.session["name"]
    path = './financial/static/financial/img/' + username
    pathList = glob.glob(path + '/'+basename+'*.png')
    if len(pathList) == 0:
        return ""
    return os.path.basename(pathList[0])


def getImgRatio(request, balanceType):
    import math
    username = request.session["name"]
    maxRatio = 2.0
    sumIncome = 0
    sumExpence = 0
    for balance in Balance.objects.filter(userName=username):
        if balance.isIncome:
            sumIncome += balance.amount
        else:
            sumExpence += balance.amount
    ratio = 1.0
    if sumIncome > 0 and sumExpence > 0:
        if balanceType == "income":
            ratio = sumIncome/math.sqrt(sumIncome*sumExpence)
        else:
            ratio = sumExpence/math.sqrt(sumIncome*sumExpence)
    if math.sqrt(maxRatio) < ratio:
        ratio = math.sqrt(maxRatio)
    elif ratio < 1/math.sqrt(maxRatio):
        ratio = 1/math.sqrt(maxRatio)
    return ratio


def createIncomeCircle(request):
    import os
    import glob
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.font_manager import FontProperties
    fp = FontProperties(fname='./financial/static/financial/ttf/ipag.ttf');
    username = request.session["name"]
    incomes = Balance.objects.filter(isIncome=True, userName=username)

    # フォルダ作成、既存のファイル削除
    path = './financial/static/financial/img/' + username
    if not os.path.isdir(path):
        os.makedirs(path, exist_ok=True)
    else:
        fileList = glob.glob(path + '/circle_income*.png')
        for file in fileList:
            os.remove(file)
    # 画像生成
    if len(incomes) > 0:
        d = {}
        for income in incomes:
            if income.categoryName in d:
                d[income.categoryName] += income.amount
            else:
                d[income.categoryName] = income.amount
        d = dict(sorted(d.items(), key=lambda x: -x[1]))
        label = d.keys()
        amount = d.values()
        plt.clf()
        fig = plt.figure(figsize=(4, 3))
        fig.patch.set_alpha(0)
        ax = fig.add_subplot(111)
        ax.axis("equal")
        patches, texts, autotexts = ax.pie(amount,  # データ
                    startangle=90,  # 円グラフ開始軸を指定
                    #labels=label,  # ラベル
                    autopct = lambda p: '{:.1f}%'.format(p) if p >= 5 else '',  # パーセント表示
                   # colors=colors,  # 色指定
                    counterclock=False,  # 逆時計回り
                    radius=getImgRatio(request, "income"),  # 半径
                    )
        plt.legend(label, bbox_to_anchor=(0.5, -0.1), prop=fp, loc='upper center', borderaxespad=0,
                   ncol=4)
        plt.setp(texts, fontproperties=fp)
        plt.suptitle('収入', size=256, fontproperties = fp)
        plt.subplots_adjust(bottom=0.25)
        plt.tight_layout()
        # 保存
        time = datetime.datetime.today().strftime("%Y%m%d%H%M%S")
        plt.savefig(path+'/circle_income'+time+'.png')


def createExpenceCircle(request):
    import os
    import glob
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.font_manager import FontProperties
    fp = FontProperties(fname='./financial/static/financial/ttf/ipag.ttf');
    username = request.session["name"]
    expences = Balance.objects.filter(isIncome=False, userName=username)

    # フォルダ作成、既存のファイル削除
    path = './financial/static/financial/img/' + username
    if not os.path.isdir(path):
        os.makedirs(path, exist_ok=True)
    else:
        fileList = glob.glob(path + '/circle_expence*.png')
        for file in fileList:
            os.remove(file)
    # 画像生成
    if len(expences) > 0:
        d = {}
        for expence in expences:
            if expence.categoryName in d:
                d[expence.categoryName] += expence.amount
            else:
                d[expence.categoryName] = expence.amount
        d = dict(sorted(d.items(), key=lambda x: -x[1]))
        label = d.keys()
        amount = d.values()
        plt.clf()
        fig = plt.figure(figsize=(4, 3))
        fig.patch.set_alpha(0)
        ax = fig.add_subplot(111)
        ax.axis("equal")
        patches, texts, autotexts = ax.pie(amount,  # データ
                    startangle=90,  # 円グラフ開始軸を指定
                    #labels=label,  # ラベル
                                           autopct=lambda p: '{:.1f}%'.format(p) if p >= 5 else '',  # パーセント表示
                   # colors=colors,  # 色指定
                    counterclock=False,  # 逆時計回り
                    radius=getImgRatio(request, "expence"),  # 半径
                    )
        plt.legend(label, bbox_to_anchor=(0.5, -0.1), prop=fp, loc='upper center', borderaxespad=0,
                   ncol=4)
        plt.setp(texts, fontproperties=fp)
        plt.suptitle('支出', size=256, fontproperties = fp)
        plt.subplots_adjust(bottom=0.25)
        plt.tight_layout()
        # 保存
        time = datetime.datetime.today().strftime("%Y%m%d%H%M%S")
        plt.savefig(path+'/circle_expence'+time+'.png')


def createLineGraph(request):
    import numpy as np
    import os
    import glob
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.font_manager import FontProperties
    fp = FontProperties(fname='./financial/static/financial/ttf/ipag.ttf');
    username = request.session["name"]
    year = datetime.date.today().year

    # フォルダ作成、既存のファイル削除
    path = './financial/static/financial/img/' + username
    if not os.path.isdir(path):
        os.makedirs(path, exist_ok=True)
    else:
        fileList = glob.glob(path + '/monthly'+str(year)+'_*.png')
        for file in fileList:
            os.remove(file)
    balances = Balance.objects.filter(userName=username)
    month = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    monthStr = map(lambda m:str(m)+'月', month)
    monthlyIncome = [0]*12
    monthlyExpence = [0]*12
    for balance in balances:
        if balance.date.year == year:
            if balance.isIncome:
                monthlyIncome[balance.date.month-1] += balance.amount
            else:
                monthlyExpence[balance.date.month-1] += balance.amount
    plt.clf()
    fig = plt.figure(figsize=(4, 3))
    fig.patch.set_alpha(0)
    ax = fig.add_subplot(111)
    ax.patch.set_alpha(0)
    ax.plot(np.array(month), np.array(monthlyIncome),
            color="blue",
            marker="D",
            markersize=4,
            markeredgewidth=2,
            markeredgecolor="blue",
            markerfacecolor="lightblue",
            )
    ax.plot(np.array(month), np.array(monthlyExpence),
            color="red",
            marker="D",
            markersize=4,
            markeredgewidth=2,
            markeredgecolor="red",
            markerfacecolor="lightcoral",
            )
    plt.xticks(month, monthStr, fontproperties=fp)
    ax.set_xlim([1, 12])
    plt.suptitle('月別グラフ（単位：円）', size=256, fontproperties=fp)
    plt.tight_layout()
    # 保存
    time = datetime.datetime.today().strftime("%Y%m%d%H%M%S")
    plt.savefig(path + '/monthly'+str(year)+'_' + time + '.png')


def income(request):
    inputIncomeStr = request.POST["income"]
    description = request.POST["incomeDescription"]
    user = request.session["name"]
    if inputIncomeStr.isdecimal() and description != "":  # 入力が数字の時
        inputIncome = int(inputIncomeStr)
        categoryName = request.POST["incomeCategory"]
        income = Balance(description=description, amount=inputIncome, isIncome=True, date=datetime.date.today(),
                         categoryName=categoryName, userName=user)
        income.save()
        # グラフの用意
        createIncomeCircle(request)
        createExpenceCircle(request)
        createLineGraph(request)
        return render(request, "income.html")
    else:  # 入力が数字でない時のエラー
        if not inputIncomeStr.isdecimal():
            return viewError(request, "incomeError", "notDecimalError")
        else:
            return viewError(request, "incomeError", "contentBlankError")


def expence(request):
    inputExpenceStr = request.POST["expence"]
    description = request.POST["expenceDescription"]
    user = request.session["name"]
    if inputExpenceStr.isdecimal() and description != "":
        inputExpence = int(inputExpenceStr)
        categoryName = request.POST["expenseCategory"]
        expence = Balance(description=description, amount=inputExpence, isIncome=False, date=datetime.date.today(),
                          categoryName=categoryName, userName=user)
        expence.save()
        # グラフの用意
        createIncomeCircle(request)
        createExpenceCircle(request)
        return render(request, "expence.html")
    else:  # 入力エラーの時
        if not inputExpenceStr.isdecimal():
            return viewError(request, "expenseError", "notDecimalError")
        else:
            return viewError(request, "expenseError", "contentBlankError")


def delete(request):
    balances = Balance.objects.all()
    user = User.objects.all()
    Categories = Category.objects.all()
    balances.delete()
    user.delete()
    Categories.delete()
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
            #return render(request, "home.html", {"name": request.session.get("name")})
            return view(request)
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
        return render(request, "signupconfirm.html")
    else:
        return render(request, "signup.html", {"error": "name"})


def signout(request):
    request.session.clear()
    return render(request, "home.html", {"name": request.session.get("name")})


def category(request):  # カテゴリー登録関数
    inputCategory = request.POST["registrationCategory"]
    categoryType = request.POST["categoryType"]
    IncomeCategory = Category.objects.filter(balance=True)
    ExpenseCategory = Category.objects.filter(balance=False)
    if inputCategory == "":
        return viewError(request, "categorySubscribeError", "blank")
    if categoryType == "income":
        if len(Category.objects.filter(categoryName=inputCategory, balance=True)) == 0:
            newcategory = Category(categoryName=inputCategory, balance=True)
            newcategory.save()
        else:
            return viewError(request, "categorySubscribeError", "duplication")
    else:
        if len(Category.objects.filter(categoryName=inputCategory, balance=False)) == 0:
            newcategory = Category(categoryName=inputCategory, balance=False)
            newcategory.save()
        else:
            return viewError(request, "categorySubscribeError", "duplication")
    return render(request, "category.html")


def viewError(request, errorName, errorType):
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
        return render(request, "view.html", {"categorySubscribeError": "blank",
                                             "incomes": incomes, "expences": expences, "sumIncomes": sumIncomes, "sumExpences": sumExpences, "gain": gain,
                                             "incomeCategories": incomeCategories, "expenseCategories": expenseCategories
                                             })
    if categoryType == "income":
        if len(Category.objects.filter(categoryName=inputCategory, balance=True)) == 0:
            newcategory = Category(categoryName=inputCategory, balance=True)
            newcategory.save()
        else:
            return render(request, "view.html", {"categorySubscribeError": "duplication", "incomes": incomes, "expences": expences, "sumIncomes": sumIncomes, "sumExpences": sumExpences, "gain": gain,
                                                 "incomeCategories": incomeCategories, "expenseCategories": expenseCategories})
    else:
        if len(Category.objects.filter(categoryName=inputCategory, balance=False)) == 0:
            newcategory = Category(categoryName=inputCategory, balance=False)
            newcategory.save()
        else:
            return render(request, "view.html", {"categorySubscribeError": "duplication", "incomes": incomes, "expences": expences, "sumIncomes": sumIncomes, "sumExpences": sumExpences, "gain": gain,
                                                 "incomeCategories": incomeCategories, "expenseCategories": expenseCategories})
    return render(request, "category.html")
