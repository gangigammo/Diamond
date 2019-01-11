from financial.models import Balance
from typing import Optional, List


class Balances():
    # 収支idから収支を取得
    @staticmethod
    def getById(id: int) -> Optional[Balance]:      # 存在しなければNoneを返す
        return Balance.objects.filter(id=id).first()

    # 収支idのリストから収支リストを取得
    @staticmethod
    def getByIdList(ids: List[int]) -> Optional[List[Balance]]:
        return Balance.objects.filter(id__in=ids)
