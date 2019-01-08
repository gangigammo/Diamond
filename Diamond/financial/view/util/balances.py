from financial.models import Balance
from typing import Optional


class Balances():
    @staticmethod
    def getById(id: int) -> Optional[Balance]:      # 存在しなければNoneを返す
        return Balance.objects.filter(id=id).first()
