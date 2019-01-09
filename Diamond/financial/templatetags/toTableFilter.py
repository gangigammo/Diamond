from django.template.defaultfilters import register
from financial.models import Balance
from typing import Union
from typing import Optional
from typing import List
from typing import Any
import inspect


rowPrefix = "<td>"
rowSuffix = "</td>"


NoneType = type(None)
DomainType = Union[Balance]


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


def __parse(value: DomainType, format: Optional[str]) -> List[str]:
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

    values = [getValue(k) for k in keys]
    return values


def __buildString(values: List[Any], prefix: str, suffix: str) -> str:
    strs = map(str, values)
    string = prefix + (suffix + prefix).join(strs) + suffix
    return string


@register.filter
def toRow(value: Optional[DomainType], format=None) -> Optional[str]:
    values = value and __parse(value, format)
    string = values and __buildString(
        values=values, prefix=rowPrefix, suffix=rowSuffix)
    return string
