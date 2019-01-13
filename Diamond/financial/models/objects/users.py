"""
金剛会計におけるユーザーを、データベースとやり取りするモジュール
"""

from .appobjects import AppObjects
from typing import Sequence
from financial.models import User


class Users(AppObjects):
    _T = User  # Override
    """
    金剛会計におけるユーザーを、データベースとやり取りするクラス

    このクラスの処理は、classmethodとして実装されています。(Javaでいうところのstatic method)
    インスタンスからではなく、クラスからメソッドを呼び出してください
    ex.> allUsers = Users.getAll()

    Attributes
    ----------
    _T : type
        financial.models.User
    """
