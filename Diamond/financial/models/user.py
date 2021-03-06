"""
ユーザーのモデル
"""
from django.db.models import Model, CharField
from django.db.models import Sum
from django.db.models.query import QuerySet
import hashlib


class User(Model):
    """
    ユーザーのモデルです

    使用例
    user = User.new(name="hoge", password="foo")
    user.setPassword(password="bar")
    user.isCorrect("nanka")
    user.delete()

    Fields
    ------
    name : CharField
        ユーザー名
    password : CharField
        パスワード
    """

    # Fields

    name = CharField(max_length=128, unique=True)
    password = CharField(max_length=128)

    # factory method
    @staticmethod
    def new(name, password):
        """
        新しいユーザーを返します

        Parameters
        ----------
        name : str
            ユーザー名
        password : str
            パスワード(平文)

        Return
        ------
        user : User
            新しいユーザー
        """
        user = User(name=name, password="none")
        user.setPassword(password=password)
        return user

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

    # private methods

    def __digest(self, password: str) -> str:
        """
        文字列をハッシュ化します

        Parameters
        ----------
        password : str
            平文のパスワード

        Returns
        -------
        digestedPassword : str
            ダイジェスト化されたパスワード
        """
        # パスワードのハッシュ化
        digested = password
        for val in range(0, 1000):
            digested = hashlib.sha256(
                (str(self.name) + digested).encode('utf-8')
            ).hexdigest()
        return digested
