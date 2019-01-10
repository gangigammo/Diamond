from django.utils.safestring import SafeText, mark_safe
from typing import Dict, Optional, Any
from django.utils.html import format_html, format_html_join


# HTMLを扱う補助メソッド


# aタグを生成
def html_a(
    content: str,    # 内容
    href: str,       # リンク
    **kwargs
) -> SafeText:
    kwargs.update({"href": href})
    return __generateHtml("a", content, **kwargs)


# tableタグを生成
def html_table(
    content: str,    # 内容
    **kwargs
) -> SafeText:
    return __generateHtml("table", content, **kwargs)


# theadタグを生成
def html_thead(
    content: str,    # 内容
    **kwargs
) -> SafeText:
    return __generateHtml("thead", content, **kwargs)


# tbodyタグを生成
def html_tbody(
    content: str,    # 内容
    **kwargs
) -> SafeText:
    return __generateHtml("tbody", content, **kwargs)


# trタグを生成
def html_tr(
    content: str,    # 内容
    **kwargs
) -> SafeText:
    return __generateHtml("tr", content, **kwargs)


# tdタグを生成
def html_td(
    content: str,    # 内容
    **kwargs
) -> SafeText:
    return __generateHtml("td", content, **kwargs)


# HTMLタグを生成
def __generateHtml(
        tag: str,       # HTMLタグ名
        content: str,   # 開始タグと終了タグの間に入る内容
        **kwargs: str   # 属性
) -> SafeText:
    htmlFormat = "<tag {}>{}</tag>".replace("tag", tag)
    attrHtml = format_html_join(
        " ", '{}="{}"', kwargs.items())
    attrHtml = attrHtml or ""
    result = format_html(htmlFormat, attrHtml, content)
    return result
