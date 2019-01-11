from financial.models import Balance
from typing import Optional, List


# 条件に一致する収支を取得するstaticメソッド群
class Balances():

    # 収支idから収支を取得
    @staticmethod
    def get(
        # 検索項目
        # hoge=None
        id=None,        # int
        writer=None     # str

    ) -> Optional[Balance]:
        ids = id and [id]
        return Balances.getlist(ids, writer).first()

    # 収支idのリストから収支リストを取得
    @staticmethod
    def getlist(
        # 検索項目
        # hoge=None
        ids=None,       # List[int]
        writer=None     # str

    ) -> List[Balance]:
        all = Balance.objects
        # 検索処理
        # byHoge = hoge and byXxxx and byXxxx.filter(hoge=hoge)
        byId = ids and all.filter(id__in=ids)
        byWriter = writer and byId and byId.filter(writer=writer)

        result = byWriter
        return result
