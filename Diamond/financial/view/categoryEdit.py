from django.shortcuts import render
import financial.views
from financial.models import User, Category

__topView = financial.views.view


# categoryedit/
def main(request):
    """
    カテゴリ編集画面
    categoryedit/
    """
    username = request.session["name"]
    user = User.objects.filter(name=username).first()
    categories = Category.objects.filter(writer=user)
    post = request.POST

    id = post.get("categoryID")
    name = post.get("categoryName")

    category = categories.filter(id=id).first()  # nullable

    error = ()
    if not category:
        # 対象のカテゴリが見つからない, 自分のものでないとき
        error = ("categorySubscribeError", "category")
    elif not name:
        # カテゴリ名が空欄のとき
        error = ("categorySubscribeError", "blank")
    else:
        category.setName(name)
        category.save()

    return __topView(request, *error)
