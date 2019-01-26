"""
カテゴリのモデル
"""
from django.db.models import Model, CharField, BooleanField
from django.db.models import ForeignKey
from django.db.models import CASCADE
from .user import User


class Category(Model):
    """
    カテゴリのモデルです

    Fields
    ------
    name : CharField
        カテゴリ名
    isIncome : BooleanField
        収入なら True
        支出なら False
    writer : User
        カテゴリの作成者

    Properties (Read Only)
    ----------------------
    categoryName : CharField
        nameと同じ
    """

    # Fields

    name = CharField(max_length=128)
    isIncome = BooleanField()
    # もとのユーザ削除時 -> このカテゴリも一緒に削除される (CASCADE)
    writer = ForeignKey(User, on_delete=CASCADE)

    class Meta:
        # 同一ユーザーが同じ名前のカテゴリを重複して持てないようにする
        unique_together = ('name', 'writer', 'isIncome')

    # properties
    @property
    def categoryName(self):
        return self.name

    # public methods

    def __str__(self):
        return self.name

    def setName(self, name: str):
        """
        カテゴリ名をセットします

        Parameters
        ----------
        name : str
            新しいカテゴリ名

        Returns
        -------
        category : Category
            このカテゴリオブジェクト
        """
        self.name = name
        return self
