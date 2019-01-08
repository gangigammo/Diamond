from django.template.defaultfilters import register
from financial.models import Balance
from typing import Union
from typing import Optional

NoneType = type(None)


# テーブルの行を生成


def __noneToRow(value: NoneType) -> str:
    return "none"


def __balanceToRow(value: Balance) -> str:
    string = value and str(value.amount) + \
        str(value.description) + str(value.categoryName)
    return string


# ディスパッチャ


__toRowMethods = {
    NoneType:   __noneToRow,
    Balance:    __balanceToRow
}


@register.filter
def toRow(value: Optional[Union[Balance]]) -> str:
    method = __toRowMethods.get(type(value))
    if (method is None):
        raise TypeError("toRowフィルタに渡す値の型が違います" + type(value))
    string = method(value)
    return string
