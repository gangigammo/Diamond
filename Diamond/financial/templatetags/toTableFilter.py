from django.template.defaultfilters import register
from financial.models import Balance
from typing import Union
from typing import Optional
from typing import List

NoneType = type(None)
DomainType = Union[Balance]


def __noneMap(v): return "none"


__mapDicts = {
    NoneType: {},
    Balance: {
        "amount":
            lambda v: v.amount,
        "description":
            lambda v: v.description,
        "category":
            lambda v: v.categoryName
    }
}

__formats = {
    NoneType: "",
    Balance: "amount description category"
}


def __parse(value: Optional[DomainType], format: Optional[str]) -> List[str]:
    valueType = type(value)
    mapDict = __mapDicts.get(valueType)
    format = format or __formats.get(valueType)
    # TODO value型エラー
    keys = format.split(" ")
    # TODO formatの間違いを例外として投げる
    values = [(mapDict.get(key) or __noneMap)(value) or "" for key in keys]
    return values


@register.filter
def toRow(value: Optional[DomainType], format=None) -> str:
    values = __parse(value, format)
    return str(values)  # TODO 文字列リストからテーブルHTMLに。
