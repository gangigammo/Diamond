"""
ユーザーのモデル
"""
from django.db.models import Model, CharField
from django.db.models import Sum
from django.db.models.query import QuerySet


class User(Model):
    """
    ユーザーのモデルです

    Fields
    ------
    name : CharField
        ユーザー名
    password : CharField
        パスワード
    """

    # Fields

    name = CharField(max_length=128)
    password = CharField(max_length=128)  # TODO 平文にしない

    # public methods

    def __str__(self):
        return str(self.name)

    def isCorrect(self, password: str) -> bool:
        """
        入力されたパスワードが正しいかどうかを返します

        Parameters
        ----------
        password : str
            パスワード(平文)

        Return
        ------
        iscorrect : bool
            正しいかどうかの論理値
        """
        digested = self.__digest(password)
        result = (self.password == digested)
        return result

    def setPassword(self, password: str):
        """
        パスワードを変更します

        Parameters
        ----------
        password : str
            新しいパスワード(平文)
        """
        self.password = self.__digest(password)

    def sum(self) -> int:
        """
        このユーザーが所持する合計を計算します

        Returns
        -------
        sum : int
            合計
        """
        balances = self.balances.all
        sum = balances.value.aggregate(Sum("amount"))
        return sum

    # private methods

    def __digest(self, password: str) -> str:
        digested = password  # TODO パスワードのダイジェスト化
        return digested
