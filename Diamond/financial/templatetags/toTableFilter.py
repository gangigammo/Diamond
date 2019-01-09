from django.template.defaultfilters import register
from financial.models import Balance
from typing import Union
from typing import Optional
from typing import List

NoneType = type(None)
DomainType = Union[Balance]

__maps = {
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
    map = __maps.get(type(value))
    format = format or __formats.get(type(value))
    keys = format.split(" ")
    # TODO formatの間違いを例外として投げる
    values = [map.get(key)(value) or "" for key in keys]
    return values


@register.filter
def toRow(value: Optional[DomainType], format=None) -> str:
    values = __parse(value, format)
    return str(values)  # TODO 文字列リストからテーブルHTMLに。
