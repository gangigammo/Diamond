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
        # TODO [読み取り専用]
        ユーザー名
    password : CharField
        # TODO [書き込み専用]
        パスワード
    """

    # private fields

    _name = CharField(max_length=128)
    _password = CharField(max_length=128)  # TODO 平文にしない　

    # accesers

    @property
    def name(self):
        return self._name

    # public methods

    def __init__(self, name: str, password: str):
        """
        Userインスタンスを生成します

        Parameters
        ----------
        name : str
            ユーザー名
        password : str
            パスワード
        """
        super().__init__(self)
        self._name = name
        self._password = self.__digest(password)

    def __str__(self):
        return str(self._name)

    # TODO password auth

    # TODO update password

    # private methods

    def __digest(self, newPassword: str) -> str:
        digested = newPassword  # TODO パスワードのダイジェスト化
        return digested
