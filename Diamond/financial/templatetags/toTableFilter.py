from django.template.defaultfilters import register
from django.utils.html import format_html, conditional_escape
from django.utils.safestring import SafeText, mark_safe

from typing import Union, Any, List, Optional, Iterable
from types import GeneratorType
from operator import add
from functools import reduce
import inspect


from .parseRules import parseRules, defaultFormats, DomainType
from .util import *


# 値 -> HTMLテーブルの行の1要素 への変換 (ex. "hoge"　-> "<td>hoge</td>")
@register.filter(is_safe=True)
def toTd(element: Optional[Any]) -> SafeText:
    return html_td(element)


# 値 -> HTMLテーブルの行要素 への変換 (<tr>...</tr>)
@register.filter(is_safe=True)
def toTr(value: Optional[DomainType], format=None) -> SafeText:
    elements = value and __parse(value, format)     # 文字列のリストを取得
    datas = elements and map(toTd, elements)        # 各要素にtoDataを適用
    return html_tr(datas)


# 値リスト -> HTMLテーブルのtbody要素 への変換 (<tbody>...</tbody>)
@register.filter(is_safe=True)
def toTbody(values: List[DomainType], format=None) -> SafeText:
    def curried_toTr(v): return toTr(v, format=format)
    rows = map(curried_toTr, values)
    return html_tbody(rows)


# 値リスト -> HTMLテーブル要素 への変換 (<table>...</table>)
@register.filter(is_safe=True)
def toTable(values: List[DomainType], format=None) -> SafeText:
    tbody = toTbody(values, format)
    return html_table(tbody)


# テーブルにtheadを加える
@register.filter(is_safe=True)
def addThead(base: SafeText, titles: str):
    (body, attr) = unwrapHtml("table", base)
    head = toThead(titles)
    return html_table(head+body, **attr)


# コンマ区切り文字列 -> テーブルのヘッダ への変換
def toThead(titles: str):
    titleList = titles.split(',')
    heads = map(html_th, titleList)
    row = html_tr(heads)
    return html_thead(row)


# 値 -> フォーマット通りの順で要素を並べたリスト への変換
def __parse(value: DomainType, format: Optional[str]) -> List[str]:
    # valueの型
    valueType = type(value)
    # valueTypeに対応する変換規則
    rule = parseRules.get(valueType)
    if rule is None:
        caller = inspect.stack()[1][3]
        raise TypeError("型" + str(valueType) + "は" + caller + "の引数として不適切です")
    # formatが与えられてなければ代わりにデフォルトのを使う
    format = format or defaultFormats.get(valueType)
    if format is None:
        raise SyntaxError("型" + str(valueType) + "のためのformatがありません")
    # コンマ区切りのformatをリスト形式へ変換
    keys = format.split(",")

    def getValue(key):  # keyをvalueに変換するクロージャ
        m = rule.get(key)
        if m is None:
            raise SyntaxError("フォーマット" + format + "の内、" + key + "が正しくありません")
        return m(value)
    # formatに沿ってvalueから値を取り出し並べる
    values = [getValue(k) for k in keys]
    return values
