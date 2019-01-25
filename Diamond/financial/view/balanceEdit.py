from django.shortcuts import render
import financial.views
from financial.models import User, Balance, Category
import datetime

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

    error = ()  # (エラー名, エラー詳細)のタプル。views.pyで処理される
    try:
        for id_fields in __parseChange(post):
            (id, (amount, description, categoryName, date)) = id_fields
            b = Balance.objects.filter(id=id).first()
            category = Category.objects.filter(
                writer=b.writer, name=categoryName).first()
            b.amount = amount
            b.description = description
            b.category = category
            b.date = date or b.date  # False(変更なし)ならそのまま
            b.save()
    except (ValueError, TypeError) as ex:
        error = ("incomeError", str(ex))
    return __topView(request, *error)


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

    # 入力が正しいかチェック
    def isValid(i):
        (id, amount, description, category, date) = (
            i[0], i[1][0], i[1][1], i[1][2], i[1][3])
        if not (id.isdecimal()):
            raise AssertionError("入力が正しく送られていません")
        if not (amount.isdecimal()):
            # viewに"incomeError"として送られるエラーメッセージ
            raise ValueError("notDecimalError")
        if not bool(description):
            raise TypeError("contentBlankError")
        if not (isValidDate(date)):
            raise ValueError("invalidDateError")
        return True

    def isValidDate(dateStr: str):
        date = datetime.date.fromisoformat(dateStr)
        today = datetime.date.today()
        isNotFuture = date and bool(date <= today)  # 未来はFalse
        # date=Noneは間違いではないのでTrue
        isNone = bool(date is None)
        return isNone or isNotFuture

    result = (i for i in input if isValid(i))

    return result
