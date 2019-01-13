"""
ユーザーのモデル
"""
from django.db.models import Model, CharField


class User(Model):
    """
    ユーザーのモデルです

    Attributes
    ----------
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
            パスワード

        Return
        ------
        iscorrect : bool
            正しいかどうかの論理値
        """
        digested = self.__digest(password)
        result = (self._password == digested)
        return result

    def update(self, **kwargs):
        """
        ユーザーの内容を変更します
        必ず名前付き引数で指定してください
        引数が省略された項目は無視されます

        Parameters
        ----------
        password : str
            新しいパスワード
        """
        keys = kwargs.keys()
        if "password" in keys:
            self.password = self.__digest(kwargs.get("password"))

    # private methods

    def __digest(self, password: str) -> str:
        digested = password  # TODO パスワードのダイジェスト化
        return digested
