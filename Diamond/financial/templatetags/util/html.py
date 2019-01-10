from django.utils.safestring import SafeText, mark_safe
from django.utils.html import format_html, format_html_join, conditional_escape
from typing import Dict, Optional, Any, Union, List, Iterable, Tuple
from types import GeneratorType
from operator import add
from functools import reduce
import re


# HTMLを扱う補助メソッド


# aタグを生成
def html_a(
    contents: str,
    href: str,       # リンク
    **kwargs
) -> SafeText:
    kwargs.update({"href": href})
    return __generateHtml("a", contents, **kwargs)


# tableタグを生成
def html_table(
    contents: str,
    **kwargs
) -> SafeText:
    return __generateHtml("table", contents, **kwargs)


# theadタグを生成
def html_thead(
    contents: str,
    **kwargs
) -> SafeText:
    return __generateHtml("thead", contents, **kwargs)


# tbodyタグを生成
def html_tbody(
    contents: str,
    **kwargs
) -> SafeText:
    return __generateHtml("tbody", contents, **kwargs)


# trタグを生成
def html_tr(
    contents: str,
    **kwargs
) -> SafeText:
    return __generateHtml("tr", contents, **kwargs)


# tdタグを生成
def html_td(
    contents: str,
    **kwargs
) -> SafeText:
    return __generateHtml("td", contents, **kwargs)


# thタグを生成
def html_th(
    contents: str,
    **kwargs
) -> SafeText:
    return __generateHtml("th", contents, **kwargs)


# HTMLタグを生成
def __generateHtml(
        tag: str,       # HTMLタグ名
        contents: str,  # 開始タグと終了タグの間に入る内容
        **kwargs: str   # 属性
) -> SafeText:
    htmlFormat = "<tag {}>{}</tag>".replace("tag", tag)
    attrHtml = format_html_join(
        " ", '{}="{}"', kwargs.items())
    attrHtml = attrHtml or ""
    contentHtml = __join(contents)
    result = format_html(htmlFormat, attrHtml, contentHtml)
    return result


def __join(text: Union[None, str, Iterable[str]]) -> SafeText:
    if isinstance(text, (list, map, GeneratorType)):
        text = reduce(add, text)
    return text or ""


# HTMLタグを外す (単純に外側の1個だけ外す)
def unwrapHtml(
    tag: str,  # HTMLタグ名
    html: SafeText
):
    safeHtml = conditional_escape(html)
    regex = r"^<tag\s?([^<]*)>(.*)</tag>$".replace("tag", tag)
    content = mark_safe(re.sub(regex, r'\2', safeHtml))
    attr = re.sub(regex, r'\1', safeHtml)
    attrs = re.findall(r"(\S+)\s*=\s*['\"](\S+)['\"]", attr)
    # attrs = [ (key,value), (key,value), ... ]
    attrDict = dict(attrs)
    return (content, attrDict)
