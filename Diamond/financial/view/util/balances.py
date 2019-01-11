from financial.models import Balance
from typing import Optional, List


class Balances():
    # 収支idから収支を取得
    @staticmethod
    def get(
        id=None,        # int
        writer=None     # str
    ) -> Optional[Balance]:
        ids = id and [id]
        return Balances.getlist(ids, writer).first()

    # 収支idのリストから収支リストを取得
    @staticmethod
    def getlist(
        ids=None,       # List[int]
        writer=None     # str
    ) -> List[Balance]:
        all = Balance.objects
        byId = ids and all.filter(id__in=ids)
        result = writer and byId and byId.filter(writer=writer)
        return result
