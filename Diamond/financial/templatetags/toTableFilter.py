from django.template.defaultfilters import register
from financial.models import Balance
from typing import Union
from typing import Optional
from typing import List

NoneType = type(None)


# テーブルの行を生成


def __parseNone(value: NoneType) -> List[str]:
    return ["none"]


def __parseBalance(value: Balance, format="amount description category") -> List[str]:
    if not type(value) is Balance:
        raise TypeError
    valueDic = {
        "amount": value.amount,
        "description": value.description,
        "category": value.categoryName
    }
    keys = format.split(" ")
    values = [valueDic.get(key) for key in keys]
    return values


# ディスパッチャ


__parseMethods = {
    NoneType:   __parseNone,
    Balance:    __parseBalance
}


@register.filter
def toRow(value: Optional[Union[Balance]]) -> str:
    method = __parseMethods.get(type(value))
    if (method is None):
        raise TypeError("toRowフィルタに渡す値の型が違います" + type(value))
    values = method(value)
    return str(values)
