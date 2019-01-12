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
        [読み取り専用]
        ユーザー名
    password : CharField
        [書き込み専用]
        パスワード
    """

    # private fields

    _name = CharField(max_length=128)
    _password = CharField(max_length=128)  # TODO 平文にしない　

    # accesers

    @property
    def name(self):
        return self._name

    @password.setter
    def password(self, password: str):
        self._password = self.__digest(password)

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

    def update(self, password=None):
        """
        ユーザーの内容を変更します
        引数が省略されるかNoneである項目は無視されます

        Parameters
        ----------
        password : str or None
            新しいパスワード
        """
        if password:
            self.password = password  # setterを呼んでいる

    # private methods

    def __digest(self, password: str) -> str:
        digested = password  # TODO パスワードのダイジェスト化
        return digested
