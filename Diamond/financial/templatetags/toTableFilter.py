from django.template.defaultfilters import register
from financial.models import Balance
from typing import Union
from typing import Optional
from typing import List

NoneType = type(None)


# テーブルの行を生成


def __parseNone(value: NoneType, format: str) -> List[str]:
    return ["none"]  # TODO 要素数を揃える


# TODO デフォルト引数を吟味
def __parseBalance(value: Balance, format="amount description category") -> List[str]:
    if not type(value) is Balance:
        raise TypeError
    valueDic = {
        "amount": value.amount,
        "description": value.description,
        "category": value.categoryName
    }
    # TODO フォーマット文字列の例外処理
    keys = format.split(" ")    # TODO split処理を別メソッドに分ける
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
    return str(values)  # TODO 文字列リストからテーブルHTMLに。
