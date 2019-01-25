from django.shortcuts import render
import financial.views
from financial.models import User, Balance, Category

__topView = financial.views.view


# ディスパッチャ    balanceedit/
def main(request):
    username = request.session["name"]              # 自分のユーザー名
    user = User.objects.filter(name=username).first()
    selects = __getSelects(request, user)
    keys = request.POST.keys()

    # keys の文字列によって操作を場合分け
    if "delete" in keys:
        result = __delete(request, user, selects)
    elif "change" in keys:
        result = __change(request, user, selects)
    # TODO elifで他のメソッドを追加

    result = result or __topView(request)
    return result


# チェックボックスで選択した収支リストを取得
def __getSelects(request, user):
    query = request.POST
    ids = query.getlist("balanceSelect")            # 収支idリスト
    selects = Balance.objects.filter(id__in=ids,    # idリストから収支を取得
                                     writer=user)   # 他人の収支は除く
    return selects


# 収支を削除
def __delete(request, user, selects):
    for g in selects:
        g.delete()
    return __topView(request)


# 収支を編集
def __change(request, user, selects):
    responseDict = {
        "selects": selects,
        "incomeCategories": Category.objects.filter(writer=user, isIncome=True),
        "expenseCategories": Category.objects.filter(writer=user, isIncome=False)
    }
    return render(request, "changeBalance.html", responseDict)


# 編集を適用    balanceedit/apply/
def apply(request):
    post = request.POST
    for id_fields in __parseChange(post):
        (id, (amount, description, categoryName, date)) = id_fields
        b = Balance.objects.filter(id=id).first()
        category = Category.objects.filter(
            writer=b.writer, name=categoryName).first()
        b.amount = amount
        b.description = description
        b.category = category
        b.date = date
        b.save()
    return __topView(request)


def __parseChange(dic):
    """
    {
        "id-amount": value, ...
    }
    の辞書を、
    ((id, (amount,description,categoryName,date)), ...)
    のタプルへ変換する。
    空欄や、金額が数字以外である項目は無視する
    """
    # (id, ...) : tuple[str]
    ids = (i.rstrip("-amount")
           for i in dic.keys() if i.endswith("-amount"))
    # POSTされた入力の取り出し
    input = [(
        i,
        (
            dic.get(i + "-amount"),
            dic.get(i + "-description"),
            dic.get(i + "-category"),
            dic.get(i + "-date")
        )
    ) for i in ids]
    # check
    result = (i for i in input
              if i[0].isdecimal() and i[1][0].isdecimal() and bool(i[1][1]) and bool(i[1][3])
              )
    return result
