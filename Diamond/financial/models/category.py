"""
カテゴリのモデル
"""
from django.db.models import Model, CharField, BooleanField
from django.db.models import ForeignKey
from django.db.models import CASCADE
from .user import User


class Category(Model):
    """
    カテゴリのクラスです

    Attributes
    ----------
    name : CharField
        カテゴリ名
    isIncome : BooleanField
        収入なら True
        支出なら False
    writer : User
        カテゴリの作成者
    """

    # Fields

    name = CharField(max_length=128)
    isIncome = BooleanField()
    # もとのユーザ削除時 -> このカテゴリも一緒に削除される (CASCADE)
    writer = ForeignKey(User, on_delete=CASCADE)

    # public methods

    def __str__(self):
        return self.name

    def update(self, **kwargs):
        """
        カテゴリの内容を変更します
        必ず名前付き引数で指定してください
        引数が省略された項目は無視されます

        Parameters
        ----------
        name : str
            新しいカテゴリ名
        """
        keys = kwargs.keys()
        if "name" in keys:
            self.name = kwargs.get("name")
