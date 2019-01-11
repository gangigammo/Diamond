import financial.views
from .util import *

__topView = financial.views.view


def main(request):
    # TODO ディスパッチ方法の洗練化
    methodDict = {
        "delete": __delete
    }
    methods = [*request.POST]
    methods.remove("csrfmiddlewaretoken")
    print(methods)
    if len(methods) == 1:
        method = methodDict.get(methods.pop())
    else:
        method = None
    method = method or __pass
    return method(request)


def __pass(request):
    return __topView(request)


def __delete(request):
    # TODO garbageNumsが取得できない
    garbageNums = request.POST["balance_select"]
    garbages = Balances.getByIdList(garbageNums)
    print(garbageNums)
    print(list(garbages))
    for g in garbages:
        g.delete()
    return __topView(request)
