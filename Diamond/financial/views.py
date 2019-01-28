from django.shortcuts import render
from django.shortcuts import redirect
from financial.models import *
import Diamond.settings as setting
import datetime

# Create your views here.


def home(request):
    return render(request, "home.html", {"name": request.session.get("name")})


def view(request, *args):
    import matplotlib
    matplotlib.use('Agg')
    username = request.session["name"]
    if request.method == 'POST':
        if 'Category' in request.POST:
            categoryName = request.POST["Category"]
            balances = Balance.objects.filter(
                categoryName=categoryName, writer=username)
        else:
            balances = Balance.objects.filter(writer=username)
    else:
        balances = Balance.objects.filter(writer=username)

    incomes = []
    expences = []
    categories = Category.objects.filter(writer=username)
    incomeCategories = Category.objects.filter(balance=True, writer=username)
    expenseCategories = Category.objects.filter(balance=False, writer=username)
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

    if len(args) >= 2:  # 入力内容によるエラー表示
        return render(request, "view.html",
                      {args[0]: args[1], "name": request.session.get("name"), "balances": balances, "gain": gain,
                       "incomeCategories": incomeCategories, "expenseCategories": expenseCategories,
                       "Category": categories})
    else:
        filedict = dict([(name[7:name.find('_')], name) for name in getFileName(request, 'monthly')])
        filedict = dict(sorted(filedict.items(), key=lambda x: -int(x[0])))
        print(filedict)
        return render(request, "view.html",
                      {"name": request.session.get("name"), "balances": balances, "gain": gain,
                       "incomeCategories": incomeCategories, "expenseCategories": expenseCategories,
                       "Category": categories,
                       "incomeFileName": getFileName(request, 'circle_income')[0],
                       "expenceFileName": getFileName(request, 'circle_expence')[0],
                       "lineFileName_M_dict": filedict,
                       })



def getFileName(request, basename):
    # 更新日を付与した画像のファイル名を返す
    import os
    import glob
    username = request.session["name"]
    path = setting.BASE_DIR+'/financial/static/financial/img/' + username
    pathList = glob.glob(path + '/'+basename+'*.png')
    pathList = [os.path.basename(str) for str in pathList]
    if len(pathList) == 0:
        pathList = [""]
    return pathList


def getImgRatio(request, balanceType):
    import math
    username = request.session["name"]
    maxRatio = 2.0
    sumIncome = 0
    sumExpence = 0
    for balance in Balance.objects.filter(writer=username):
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
    fp = FontProperties(fname=setting.BASE_DIR+'/financial/static/financial/ttf/ipag.ttf');
    username = request.session["name"]
    incomes = Balance.objects.filter(isIncome=True, writer=username)

    # フォルダ作成、既存のファイル削除
    path = setting.BASE_DIR+'/financial/static/financial/img/' + username
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
        fig = plt.figure(figsize=(4, 4))
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
        plt.title('収入', fontproperties = fp, fontsize=24)
        plt.subplots_adjust(bottom=0.25)


        # 保存
        plt.tight_layout()
        time = datetime.datetime.today().strftime("%Y%m%d%H%M%S")
        plt.savefig(path+'/circle_income'+time+'.png')


def createExpenceCircle(request):
    import os
    import glob
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.font_manager import FontProperties
    fp = FontProperties(fname=setting.BASE_DIR+'/financial/static/financial/ttf/ipag.ttf');
    username = request.session["name"]
    expences = Balance.objects.filter(isIncome=False, writer=username)

    # フォルダ作成、既存のファイル削除
    path = setting.BASE_DIR+'/financial/static/financial/img/' + username
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
        fig = plt.figure(figsize=(4, 4))
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
        plt.title('支出', fontproperties = fp, fontsize=24)
        plt.subplots_adjust(bottom=0.25)
        plt.tight_layout()
        # 保存
        time = datetime.datetime.today().strftime("%Y%m%d%H%M%S")
        plt.savefig(path+'/circle_expence'+time+'.png')

def createLineGraph(request):
    createMonthlyLineGraph(request, datetime.date.today().year)


def createMonthlyLineGraph(request, year):
    import numpy as np
    import os
    import glob
    import matplotlib
    import math
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.font_manager import FontProperties
    fp = FontProperties(fname=setting.BASE_DIR+'/financial/static/financial/ttf/ipag.ttf');
    username = request.session["name"]

    # フォルダ作成、既存のファイル削除
    path = setting.BASE_DIR+'/financial/static/financial/img/' + username
    if not os.path.isdir(path):
        os.makedirs(path, exist_ok=True)
    else:
        fileList = glob.glob(path + '/monthly'+str(year)+'_*.png')
        for file in fileList:
            os.remove(file)
    balances = Balance.objects.filter(writer=username)
    month = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    monthStr = map(lambda m: str(m), month)
    monthlyIncome = [0]*(datetime.date.today().month if year == datetime.date.today().year else 12)
    monthlyExpence = [0]*(datetime.date.today().month if year == datetime.date.today().year else 12)
    for balance in balances:
        if balance.date.year == year:
            if balance.isIncome:
                monthlyIncome[balance.date.month-1] += balance.amount
            else:
                monthlyExpence[balance.date.month-1] += balance.amount
    plt.clf()
    fig = plt.figure(figsize=(4, 4))
    fig.patch.set_alpha(0)
    ax = fig.add_subplot(111)
    ax.patch.set_alpha(0)
    p1 = ax.plot(np.array(month[0:datetime.date.today().month]), np.array(monthlyIncome),
            color="blue",
            marker="D",
            linewidth=3,
            markersize=6,
            markeredgewidth=2,
            markeredgecolor="blue",
            markerfacecolor="lightblue",
            )
    p2 = ax.plot(np.array(month[0:datetime.date.today().month]), np.array(monthlyExpence),
            color="red",
            marker="D",
            linewidth= 2,
            markersize=4,
            markeredgewidth=2,
            markeredgecolor="red",
            markerfacecolor="lightcoral",
            )
    plt.legend((p1[0], p2[0]), ("収入", "支出"), bbox_to_anchor=(0.5, -0.2), prop=fp, loc='upper center',
               borderaxespad=0, ncol=2)
    plt.xticks(month, monthStr, fontproperties=fp)
    plt.xlabel("月", fontproperties=fp)
    ax.set_xlim([0, 13])
    plt.title(str(year)+'年 月別グラフ', fontproperties=fp, fontsize=16)

    # y軸目盛の間隔決定
    maxval = max(monthlyIncome+monthlyExpence)
    minval = min(monthlyIncome+monthlyExpence)
    digit = len(str(maxval - minval))-2
    minval = math.ceil(minval/(10**digit)-1) * (10**digit)
    if minval < 0:
        minval = 0
    maxval = math.floor(maxval/(10**digit)+1) * (10**digit)
    ax.set_ylim([minval, maxval])
    plt.tight_layout()
    # 保存
    time = datetime.datetime.today().strftime("%Y%m%d%H%M%S")
    plt.savefig(path + '/monthly'+str(year)+'_' + time + '.png',bbox_inches='tight')



def income(request):
    inputIncomeStr = request.POST["income"]
    description = request.POST["incomeDescription"]
    if inputIncomeStr.isdecimal() and description != "":  # 入力が数字の時
        inputIncome = int(inputIncomeStr)
        categoryName = request.POST["incomeCategory"]
        username = request.session["name"]
        income = Balance(description=description, amount=inputIncome, isIncome=True, date=datetime.date.today(),
                         categoryName=categoryName, writer=username)
        income.save()
        # グラフの用意
        createIncomeCircle(request)
        createExpenceCircle(request)
        createLineGraph(request)
        return render(request, "income.html")
    else:  # 入力が数字でない時のエラー
        if not inputIncomeStr.isdecimal():
            return view(request, "incomeError", "notDecimalError")
        else:
            return view(request, "incomeError", "contentBlankError")


def expence(request):
    inputExpenceStr = request.POST["expence"]
    description = request.POST["expenceDescription"]
    if inputExpenceStr.isdecimal() and description != "":
        inputExpence = int(inputExpenceStr)
        categoryName = request.POST["expenseCategory"]
        username = request.session["name"]
        expence = Balance(description=description, amount=inputExpence, isIncome=False, date=datetime.date.today(),
                          categoryName=categoryName, writer=username)
        expence.save()
        # グラフの用意
        createIncomeCircle(request)
        createExpenceCircle(request)
        createLineGraph(request)
        return render(request, "expence.html")
    else:  # 入力エラーの時
        if not inputExpenceStr.isdecimal():
            return view(request, "expenseError", "notDecimalError")
        else:
            return view(request, "expenseError", "contentBlankError")


def delete(request):
    balances = Balance.objects.all()
    user = User.objects.all()
    category = Category.objects.all()
    balances.delete()
    user.delete()
    category.delete()
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
    username = request.session["name"]
    if inputCategory == "":
        return view(request, "categorySubscribeError", "blank")
    if categoryType == "income":
        if len(Category.objects.filter(categoryName=inputCategory, balance=True, writer=username)) == 0:
            newcategory = Category(
                categoryName=inputCategory, balance=True, writer=username)
            newcategory.save()
        else:
            return view(request, "categorySubscribeError", "duplication")
    else:
        if len(Category.objects.filter(categoryName=inputCategory, balance=False, writer=username)) == 0:
            newcategory = Category(
                categoryName=inputCategory, balance=False, writer=username)
            newcategory.save()
        else:
            return view(request, "categorySubscribeError", "duplication")
    return render(request, "category.html")
