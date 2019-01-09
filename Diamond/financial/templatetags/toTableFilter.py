from django import template
from django.utils.html import conditional_escape
from django.utils.safestring import SafeText
from django.utils.safestring import mark_safe
from django.utils.html import format_html
from financial.models import Balance
from typing import *
from types import GeneratorType
import inspect
from operator import add
from functools import reduce
import re

register = template.Library()

# HTMLコード
dataHtmlFormat = "<td>{}</td>"
rowHtmlFormat = "<tr>{}</tr>"
tbodyHtmlFormat = "<tbody>{}</tbody>"
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


# elementをhtmlFormatに従ってタグで囲む
# elementはリストでもよい
# ex. ["<td>foo</td>", "<td>bar</td>"] -> "<tr><td>foo</td><td>bar</td></tr>"
def __wrapTag(element: Union[None, SafeText, Iterable[SafeText]], htmlFormat: str) -> SafeText:
    if isinstance(element, (list, map, GeneratorType)):
        element = reduce(add, element)
    element = element or ""
    return format_html(htmlFormat, element)


# タグを除去する。(__wrapTagの逆の処理)
def __unwrapTag(html: SafeText, htmlFormat: str) -> SafeText:
    placeHolder = "{}"
    placeHolder = re.escape(placeHolder)
    htmlFormat = re.escape(htmlFormat)
    regex = htmlFormat.replace(placeHolder, "(.*)")
    result = re.sub(regex, r'\1', html)
    return mark_safe(result)


# 値 -> HTMLテーブルの行の1要素 への変換 (ex. "hoge"　-> "<td>hoge</td>")
@register.filter(is_safe=True)
def toData(element: Optional[Any]) -> SafeText:
    safeElem = __toSafeText(element)
    return format_html(dataHtmlFormat, safeElem)


# 値 -> HTMLテーブルの行要素 への変換 (<tr>...</tr>)
@register.filter(is_safe=True)
def toRow(value: Optional[DomainType], format=None) -> SafeText:
    elements = value and __parse(value, format)     # 文字列のリストを取得
    datas = elements and map(toData, elements)      # 各要素にtoDataを適用
    result = __wrapTag(datas, rowHtmlFormat)        # 行タグを付ける
    return result


# 値リスト -> HTMLテーブルのtbody要素 への変換 (<tbody>...</tbody>)
@register.filter(is_safe=True)
def toTbody(values: List[DomainType], format=None) -> SafeText:
    def curriedToRow(v): return toRow(v, format=format)
    rows = map(curriedToRow, values)
    result = __wrapTag(rows, tbodyHtmlFormat)
    return result


# 値リスト -> HTMLテーブル要素 への変換 (<table>...</table>)
@register.filter(is_safe=True)
def toTable(values: List[DomainType], format=None) -> SafeText:
    tbody = toTbody(values, format)
    result = __wrapTag(tbody, tableHtmlFormat)
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
