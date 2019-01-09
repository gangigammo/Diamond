from django.template.defaultfilters import register
from django.utils.html import format_html, conditional_escape
from django.utils.safestring import SafeText, mark_safe

from typing import Union, Any, List, Optional, Iterable
from types import GeneratorType
from operator import add
from functools import reduce
import inspect
import re


from .parseRules import parseRules, defaultFormats, DomainType


# HTMLコード
dataHtmlFormat = "<td>{}</td>"
rowHtmlFormat = "<tr>{}</tr>"
tbodyHtmlFormat = "<tbody>{}</tbody>"
theadHtmlFormat = "<thead>{}</thead>"
tableHtmlFormat = "<table>{}</table>"


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
    regex = "^(" + htmlFormat.replace(placeHolder, ")(.*)(") + ")$"
    result = re.sub(regex, r'\2', html)
    return mark_safe(result)


# 値 -> HTMLテーブルの行の1要素 への変換 (ex. "hoge"　-> "<td>hoge</td>")
@register.filter(is_safe=True)
def toData(element: Optional[Any]) -> SafeText:
    safeElem = __toSafeText(element)
    return format_html(dataHtmlFormat, safeElem)


# 値 -> HTMLテーブルの行要素 への変換 (<tr>...</tr>)
@register.filter(is_safe=True)
def toRow(value: Optional[DomainType], format=None) -> SafeText:
    elements = value and __parse(value, format)  # 文字列のリストを取得
    result = __listToRow(elements)
    return result


# 文字列リスト -> HTMLテーブルの行要素 への変換
def __listToRow(elements: List[SafeText]) -> SafeText:
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


# テーブルにtheadを加える
@register.filter(is_safe=True)
def addThead(base: SafeText, titles: str):
    body = __unwrapTag(base, tableHtmlFormat)
    head = toThead(titles)
    result = __wrapTag(head+body, tableHtmlFormat)
    return result


# コンマ区切り文字列 -> テーブルのヘッダ への変換
def toThead(titles: str):
    titleList = titles.split(',')
    row = __listToRow(titleList)
    result = __wrapTag(row, theadHtmlFormat)
    return result


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
