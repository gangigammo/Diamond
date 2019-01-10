from django.utils.safestring import SafeText, mark_safe
from typing import Dict, Optional, Any
from django.utils.html import format_html, format_html_join


# HTMLを扱う補助メソッド


# aタグを生成
def html_a(
    content: str,    # 内容
    href: str,      # リンク
) -> SafeText:
    attr = {"href": href}
    return __generateHtml("a", content, attr)


# HTMLタグを生成
def __generateHtml(
        tag: str,                               # HTMLタグ名
        content: str,                           # 開始タグと終了タグの間に入る内容
        attrs: Optional[Dict[str, Any]]          # 属性
) -> SafeText:
    htmlFormat = "<tag {}>{}</tag>".replace("tag", tag)
    attrHtml = attrs and format_html_join(
        " ", '{}="{}"', attrs.items())
    attrHtml = attrHtml or ""
    result = format_html(htmlFormat, attrHtml, content)
    return result
