import financial.views
from financial.models import User, Balance

__topView = financial.views.view


# ディスパッチャ
def main(request):
    selects = __getSelects(request)
    keys = request.POST.keys()

    # keys の文字列によって操作を場合分け
    if "delete" in keys:
        result = __delete(request, selects)
    # TODO elifで他のメソッドを追加

    result = result or __topView(request)
    return result


# チェックボックスで選択した収支リストを取得
def __getSelects(request):
    username = request.session["name"]  # 自分のユーザー名
    user = User.objects.filter(name=username).first()
    query = request.POST
    ids = query.getlist("balanceSelect")            # 収支idリスト
    selects = Balances.get(id__in=ids,              # idリストから収支を取得
                                     writer=user)   # 他人の収支は除く
    return selects


# 収支を削除
def __delete(request, selects):
    for g in selects:
        g.delete()
    return __topView(request)
