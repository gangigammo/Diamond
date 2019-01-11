from financial.models import Balance
from typing import Optional, List


# 条件に一致する収支を取得するstaticメソッド群
class Balances():
    # 収支idから収支を取得
    @staticmethod
    def get(
        id=None,        # int
        writer=None     # str
        # TODO 検索項目を追加できる

    ) -> Optional[Balance]:
        ids = id and [id]
        return Balances.getlist(ids, writer).first()

    # 収支idのリストから収支リストを取得
    @staticmethod
    def getlist(
        ids=None,       # List[int]
        writer=None     # str
        # TODO 検索項目

    ) -> List[Balance]:
        all = Balance.objects
        byId = ids and all.filter(id__in=ids)
        byWriter = writer and byId and byId.filter(writer=writer)
        # TODO 追加の検索

        result = byWriter
        return result
