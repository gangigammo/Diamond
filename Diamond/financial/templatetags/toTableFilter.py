from django.template.defaultfilters import register
from financial.models import Balance
from typing import Union
from typing import Optional
from typing import List

NoneType = type(None)


# テーブルの行を生成

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


def __parse(value, format=None):
    map = __maps.get(type(value))
    format = format or __formats.get(type(value))
    keys = format.split(" ")
    # TODO formatの間違いを例外として投げる
    values = [map.get(key)(value) or "" for key in keys]
    return values


@register.filter
def toRow(value: Optional[Union[Balance]]) -> str:
    values = __parse(value)
    return str(values)  # TODO 文字列リストからテーブルHTMLに。
