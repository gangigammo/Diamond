from django.shortcuts import render
from django.http.response import HttpResponse
import financial.views
from financial.models import User, Category
from typing import Optional

__topView = financial.views.view


# categoryedit/
def main(request) -> HttpResponse:
    """
    カテゴリ編集画面
    categoryedit/
    """
    # プルダウンで選択されたカテゴリオブジェクトを取得
    select = __getSelect(request)
    error = () if select else ("categorySubscribeError", "category")

    # 押したボタンによって操作を場合分け
    keys = request.POST.keys()
    if not select:  # カテゴリが正しく選択されていないとき
        result = __topView(request, *error)
    elif "delete" in keys:
        result = __delete(request, category=select)
    elif "change" in keys:
        result = __change(request, category=select)

    return result


def __getSelect(request) -> Optional[Category]:
    """
    プルダウンで選択されたカテゴリを、DBから取得する。
    自分の所有するカテゴリでない場合は取得しない。

    Returns
    -------
    select : Category or None
        選択されたカテゴリ
    """
    username = request.session["name"]
    user = User.objects.filter(name=username).first()
    id = request.POST.get("categoryID")
    select = Category.objects.filter(writer=user, id=id).first()
    return select


def __change(request, category: Category) -> HttpResponse:
    """
    カテゴリ名を変更し、DBへ保存する処理。

    Returns
    -------
    result
        トップページ
    """
    name = request.POST.get("categoryName")
    changedCategory = category.setName(name)
    changedCategory and changedCategory.save()
    error = () if changedCategory else ("categorySubscribeError", "blank")
    return __topView(request, *error)


def __delete(request, category: Category) -> HttpResponse:
    """
    カテゴリを削除する処理。

    Returns
    -------
    result
        トップページ
    """
    category.delete()
    return __topView(request)
