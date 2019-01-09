from django.template.defaultfilters import register
from financial.models import Balance
from typing import Union
from typing import Optional
from typing import List
import inspect

NoneType = type(None)
DomainType = Union[Balance]


def __noneMap(v): return None


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
    Balance: "amount,description,category"
}


def __parse(value: Optional[DomainType], format: Optional[str]) -> Optional[List[str]]:
    valueType = type(value)

    mapDict = __mapDicts.get(valueType)
    if mapDict is None:
        caller = inspect.stack()[1][3]
        raise TypeError("型" + str(valueType) + "は" + caller + "の引数として不適切です")

    format = format or __formats.get(valueType)
    if format is None:
        raise SyntaxError("型" + str(valueType) + "のためのformatがありません")

    keys = format.split(",")

    def getValue(key):  # keyをvalueに変換するクロージャ
        m = mapDict.get(key)
        if m is None:
            raise SyntaxError("フォーマット" + format + "の内、" + key + "が正しくありません")
        return m(value)

    values = value and [getValue(k) for k in keys]
    return values


@register.filter
def toRow(value: Optional[DomainType], format=None) -> Optional[str]:
    values = __parse(value, format)
    return values and str(values)  # TODO 文字列リストからテーブルHTMLに。
