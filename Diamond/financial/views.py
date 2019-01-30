from django.shortcuts import render
from django.shortcuts import redirect
from financial.models import *
import Diamond.settings as setting
import datetime

from django.http import HttpResponse
import csv
# Create your views here.


def home(request):
    return render(request, "home.html", {"name": request.session.get("name")})


def view(request, *args):
    import matplotlib
    matplotlib.use('Agg')
    username = request.session["name"]
    user = User.objects.filter(name=username).first()
    balances = Balance.objects.filter(writer=user).order_by("id").reverse()
    searchControl = {}
    if request.method == 'POST':
        if 'selectCategory' in request.POST and 'Category' in request.POST:
            categoryName = request.POST["Category"]
            category = Category.objects.filter(
                writer=user, name=categoryName).first()
            balances = balances.filter(category=category)
            searchControl["searchSelectCategory"] = "checked"
            searchControl["searchCategory"] = categoryName
        if 'amountFrom' in request.POST:
            amountFrom = request.POST["amountFrom"]
            if amountFrom.isdecimal():
                balances = balances.filter(amount__gte=amountFrom)
                searchControl["searchAmountFrom"] = amountFrom
        if 'amountTo' in request.POST:
            amountTo = request.POST["amountTo"]
            if amountTo.isdecimal():
                balances = balances.filter(amount__lte=amountTo)
                searchControl["searchAmountTo"] = amountTo
        if 'description' in request.POST:
            description = request.POST["description"]
            if description != "":
                balances = balances.filter(description__icontains=description)
                searchControl["searchDescription"] = description
        if 'periodFrom' in request.POST:
            periodFrom = request.POST["periodFrom"]
            if periodFrom != "":
                balances = balances.filter(date__gte=periodFrom)
                searchControl["searchPeriodFrom"] = periodFrom
        if 'periodTo' in request.POST:
            periodTo = request.POST["periodTo"]
            if periodTo != "":
                balances = balances.filter(date__lte=periodTo)
                searchControl["searchPeriodTo"] = periodTo
    incomes = []
    expences = []
    categories = Category.objects.filter(
        writer=user).order_by("id").reverse()
    incomeCategories = Category.objects.filter(
        isIncome=True, writer=user).order_by("id").reverse()
    expenseCategories = Category.objects.filter(
        isIncome=False, writer=user).order_by("id").reverse()

    #categories = categories.values(
    #    'name').order_by('name').distinct()
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
        return render(request, "view.html",
                      {"name": request.session.get("name"), "balances": balances, "gain": gain,
                       "incomeCategories": incomeCategories, "expenseCategories": expenseCategories,
                       "Category": categories,
                       "incomeFileName": getFileName(request, 'circle_income'),
                       "expenceFileName": getFileName(request, 'circle_expence'),
                       "lineFileName_M": getFileName(request, 'monthly'),
                       **searchControl,
                       })


def getFileName(request, basename):
    # 更新日を付与した画像のファイル名を返す
    import os
    import glob
    username = request.session["name"]
    path = setting.BASE_DIR+'/financial/static/financial/img/' + username
    pathList = glob.glob(path + '/'+basename+'*.png')
    if len(pathList) == 0:
        return ""
    return os.path.basename(pathList[0])


def getImgRatio(request, balanceType):
    import math
    username = request.session["name"]
    user = User.objects.filter(name=username).first()
    maxRatio = 2.0
    sumIncome = 0
    sumExpence = 0
    for balance in Balance.objects.filter(writer=user):
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
    fp = FontProperties(fname=setting.BASE_DIR +
                        '/financial/static/financial/ttf/ipag.ttf')
    username = request.session["name"]
    user = User.objects.filter(name=username).first()
    incomes = Balance.objects.filter(isIncome=True, writer=user)

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
        fig = plt.figure(figsize=(4, 3))
        fig.patch.set_alpha(0)
        ax = fig.add_subplot(111)
        ax.axis("equal")
        patches, texts, autotexts = ax.pie(amount,  # データ
                                           startangle=90,  # 円グラフ開始軸を指定
                                           # labels=label,  # ラベル
                                           autopct=lambda p: '{:.1f}%'.format(
                                               p) if p >= 5 else '',  # パーセント表示
                                           # colors=colors,  # 色指定
                                           counterclock=False,  # 逆時計回り
                                           radius=getImgRatio(
                                               request, "income"),  # 半径
                                           )
        plt.legend(label, bbox_to_anchor=(0.5, -0.1), prop=fp, loc='upper center', borderaxespad=0,
                   ncol=4)
        plt.setp(texts, fontproperties=fp)
        plt.suptitle('収入', size=256, fontproperties=fp)
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
    fp = FontProperties(fname=setting.BASE_DIR +
                        '/financial/static/financial/ttf/ipag.ttf')
    username = request.session["name"]
    user = User.objects.filter(name=username).first()
    expences = Balance.objects.filter(isIncome=False, writer=user)

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
        fig = plt.figure(figsize=(4, 3))
        fig.patch.set_alpha(0)
        ax = fig.add_subplot(111)
        ax.axis("equal")
        patches, texts, autotexts = ax.pie(amount,  # データ
                                           startangle=90,  # 円グラフ開始軸を指定
                                           # labels=label,  # ラベル
                                           autopct=lambda p: '{:.1f}%'.format(
                                               p) if p >= 5 else '',  # パーセント表示
                                           # colors=colors,  # 色指定
                                           counterclock=False,  # 逆時計回り
                                           radius=getImgRatio(
                                               request, "expence"),  # 半径
                                           )
        plt.legend(label, bbox_to_anchor=(0.5, -0.1), prop=fp, loc='upper center', borderaxespad=0,
                   ncol=4)
        plt.setp(texts, fontproperties=fp)
        plt.suptitle('支出', size=256, fontproperties=fp)
        plt.subplots_adjust(bottom=0.25)
        plt.tight_layout()
        # 保存
        time = datetime.datetime.today().strftime("%Y%m%d%H%M%S")
        plt.savefig(path+'/circle_expence'+time+'.png')


def createLineGraph(request):
    createMonthlyLineGraph(request)


def createMonthlyLineGraph(request):
    import numpy as np
    import os
    import glob
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.font_manager import FontProperties
    fp = FontProperties(fname=setting.BASE_DIR +
                        '/financial/static/financial/ttf/ipag.ttf')
    username = request.session["name"]
    user = User.objects.filter(name=username).first()
    year = datetime.date.today().year

    # フォルダ作成、既存のファイル削除
    path = setting.BASE_DIR+'/financial/static/financial/img/' + username
    if not os.path.isdir(path):
        os.makedirs(path, exist_ok=True)
    else:
        fileList = glob.glob(path + '/monthly'+str(year)+'_*.png')
        for file in fileList:
            os.remove(file)
    balances = Balance.objects.filter(writer=user)
    month = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    monthStr = map(lambda m: str(m)+'月', month)
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
            linewidth=3,
            markersize=6,
            markeredgewidth=2,
            markeredgecolor="blue",
            markerfacecolor="lightblue",
            )
    ax.plot(np.array(month), np.array(monthlyExpence),
            color="red",
            marker="D",
            linewidth=2,
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
    if inputIncomeStr.isdecimal() and description != "":  # 入力が数字の時
        inputIncome = int(inputIncomeStr)
        categoryName = request.POST["incomeCategory"]
        username = request.session["name"]
        user = User.objects.filter(name=username).first()
        category = Category.objects.filter(
            writer=user, name=categoryName).first()
        income = Balance(description=description, amount=inputIncome, isIncome=True,
                         category=category, writer=user)
        income.save()
        # グラフの用意
        createIncomeCircle(request)
        createExpenceCircle(request)
        createLineGraph(request)
        return view(request)
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
        user = User.objects.filter(name=username).first()
        category = Category.objects.filter(
            writer=user, name=categoryName).first()
        expence = Balance(description=description, amount=inputExpence, isIncome=False,
                          category=category, writer=user)
        expence.save()
        # グラフの用意
        createIncomeCircle(request)
        createExpenceCircle(request)
        return view(request)
    else:  # 入力エラーの時
        if not inputExpenceStr.isdecimal():
            return view(request, "expenseError", "notDecimalError")
        else:
            return view(request, "expenseError", "contentBlankError")


def signin(request):
    return render(request, "signin.html", {"error": "none"})


def signup(request):
    return render(request, "signup.html", {"error": "none"})


def signinconfirm(request):
    name = request.POST["name"]
    password = request.POST["password"]
    if len(User.objects.filter(name=name)) != 0:
        user = User.objects.filter(name=name)[0]
        if user.isCorrect(password=password):
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
        user = User.new(name=name, password=password)  # パスワードのハッシュ化込みでユーザー作成
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
    IncomeCategory = Category.objects.filter(isIncome=True)
    ExpenseCategory = Category.objects.filter(isIncome=False)
    username = request.session["name"]
    user = User.objects.filter(name=username).first()
    if inputCategory == "":
        return view(request, "categorySubscribeError", "blank")
    if categoryType == "income":
        if len(Category.objects.filter(name=inputCategory, isIncome=True, writer=user)) == 0:
            newcategory = Category(
                name=inputCategory, isIncome=True, writer=user)
            newcategory.save()
        else:
            return view(request, "categorySubscribeError", "duplication")
    else:
        if len(Category.objects.filter(name=inputCategory, isIncome=False, writer=user)) == 0:
            newcategory = Category(
                name=inputCategory, isIncome=False, writer=user)
            newcategory.save()
        else:
            return view(request, "categorySubscribeError", "duplication")
    return view(request)


def export(request):  # csvファイルをエクスポート
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="data.csv"'
    writer = csv.writer(response)
    username = request.session.get("name")
    user = User.objects.filter(name=username).first()
    balances = Balance.objects.filter(writer=user).order_by(
        "id").reverse()  # あとで日付順にソートすべき
    for balance in balances:  # 今は収支、内容、カテゴリーのみ。後で追加
        if(balance.isIncome):
            writer.writerow(
                [balance.amount, balance.description, balance.categoryName])
        else:
            writer.writerow(
                [-balance.amount, balance.description, balance.categoryName])
    return response

def passwordchange(request):
    return render(request, "passwordchange.html")

def passwordchangeconfirm(request):
    username = request.session["name"]
    user = User.objects.filter(name=username).first()

    oldpassword = request.POST["oldpassword"]
    newpassword = request.POST["newpassword"]

    if user.isCorrect(oldpassword):
        user.setPassword(newpassword)
        user.save()
        return view(request)
    else:
        return render(request, "passwordchange.html", {"error": "oldpassword"})


def unregister(request):
    return render(request, "unregister.html")


def unregisterconfirm(request):
    username = request.session["name"]
    user = User.objects.filter(name=username).first()
    user.delete()
    request.session.clear()
    return render(request, "home.html")
