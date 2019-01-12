"""
収支を取得するためのメソッド群
"""

from .balance import Balance
from typing import Optional, List


class Balances():
    """
    収支を取得するためのstaticメソッド群です。
    """

    @staticmethod
    def get(
        # 検索項目
        # hoge=None
        id=None,
        writer=None

    ) -> Optional[Balance]:
        """
        データベース中から、条件に一致するBalanceを1つだけ返します。
        1つもなければNoneを返します。
        引数は全て、省略可です。全て省略された場合は全ての中から1つを返します。

        Parameters
        ----------
        id : int or None
            収支ID
        writer: str or None
            収支のwriter

        Returns
        -------
        result : Balance or None
            条件に一致する収支。1つも一致しなければNone
        """

        ids = id and [id]
        return Balances.getlist(ids, writer).first()

    @staticmethod
    def getlist(
        # 検索項目
        # hoge=None
        ids=None,
        writer=None

    ) -> List[Balance]:
        """
        データベース中から、条件に一致するBalanceのリスト返します。
        1つもなければ空リストを返します。
        引数は全て、省略可です。全て省略された場合は全てのBalanceを返します。

        Parameters
        ----------
        ids : list of int or None
            収支IDのリスト
        writer : str or None
            収支のwriter

        Returns
        -------
        result_list : List[Balance]
            条件に一致する収支のリスト
        """

        all = Balance.objects
        # 検索処理
        # byHoge = hoge and byXxxx and byXxxx.filter(hoge=hoge)
        byId = ids and all.filter(id__in=ids)
        byWriter = writer and byId and byId.filter(writer=writer)

        result = byWriter
        return result
