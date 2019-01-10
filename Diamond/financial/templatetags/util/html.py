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
    attr = {"href": href}
    attr.update(kwargs)
    return __generateHtml("a", content, **attr)


# tableタグを生成
def html_table(
    content: str,    # 内容
    **kwargs
) -> SafeText:
    return __generateHtml("a", content, **kwargs)


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
