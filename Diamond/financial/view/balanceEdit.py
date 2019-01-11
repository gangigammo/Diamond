import financial.views
from .util import *

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
    query = request.POST
    ids = query.getlist("balanceSelect")
    selects = Balances.getByIdList(ids)
    # TODO 他人の収支は除外
    return selects


# 収支を削除
def __delete(request, selects):
    for g in selects:
        g.delete()
    return __topView(request)
