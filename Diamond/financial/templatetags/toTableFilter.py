from django import template
from django.utils.html import conditional_escape
from django.utils.safestring import SafeText
from django.utils.html import format_html
from financial.models import Balance
from typing import Union
from typing import Optional
from typing import List
from typing import Any
import inspect
from operator import add
from functools import reduce

register = template.Library()

# HTMLコード
# テーブルの行要素
rowPrefix = "<td>"
rowSuffix = "</td>"
dataHtmlFormat = "<td>{}</td>"
rowHtmlFormat = "<tr>{}</tr>"
tableHtmlFormat = "<table>{}</table>"


# 型の定義
NoneType = type(None)               # nullを表す
DomainType = Union[Balance]         # 引数としてとれる型一覧


# 変換規則の定義
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

# デフォルトのフォーマットの定義
# コンマ区切りで要素名を並べる
__defaultFormats = {
    NoneType: "",
    Balance: "amount,description,category"
}


def __toSafeText(element: Any) -> SafeText:
    return conditional_escape(str(element))


# 値 -> HTMLテーブルの行の1要素 への変換 (ex. "hoge"　-> "<td>hoge</td>")


@register.filter(is_safe=True)
def toData(element: Optional[Any]) -> SafeText:
    safeElem = __toSafeText(element)
    return format_html(dataHtmlFormat, safeElem)


# 値 -> HTMLテーブルの行要素 への変換 (<tr>...</tr>)
@register.filter(is_safe=True)
def toRow(value: Optional[DomainType], format=None) -> SafeText:
    elements = value and __parse(value, format)         # 文字列のリストを取得
    datas = elements and map(toData, elements)          # 各文字列にtoDataを適用
    joinedDatas = datas and reduce(add, datas)          # それらを連結
    joinedDatas = joinedDatas or ""  # valueがNoneの場合
    result = format_html(rowHtmlFormat, joinedDatas)    # 行タグを付ける
    return result


@register.filter(is_safe=True)
def toTable(values: List[DomainType], format=None) -> SafeText:
    def curriedToRow(v): return toRow(v, format=format)
    rows = map(curriedToRow, values)
    joinedRows = reduce(add, rows)
    result = format_html(tableHtmlFormat, joinedRows)
    return result


# 値 -> フォーマット通りの順で要素を並べたリスト への変換


def __parse(value: DomainType, format: Optional[str]) -> List[str]:
    # valueの型
    valueType = type(value)
    # valueTypeに対応する変換規則
    mapDict = __mapDicts.get(valueType)
    if mapDict is None:
        caller = inspect.stack()[1][3]
        raise TypeError("型" + str(valueType) + "は" + caller + "の引数として不適切です")
    # formatが与えられてなければ代わりにデフォルトのを使う
    format = format or __defaultFormats.get(valueType)
    if format is None:
        raise SyntaxError("型" + str(valueType) + "のためのformatがありません")
    # コンマ区切りのformatをリスト形式へ変換
    keys = format.split(",")

    def getValue(key):  # keyをvalueに変換するクロージャ
        m = mapDict.get(key)
        if m is None:
            raise SyntaxError("フォーマット" + format + "の内、" + key + "が正しくありません")
        return m(value)
    # formatに沿ってvalueから値を取り出し並べる
    values = [getValue(k) for k in keys]
    return values
