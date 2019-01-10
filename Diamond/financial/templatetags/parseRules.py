from django.utils.safestring import SafeText, mark_safe
from typing import Union, Dict, Optional, Any
from django.utils.html import format_html, format_html_join, conditional_escape
from financial.models import Balance

# 型の定義
NoneType = type(None)               # nullを表す
DomainType = Union[Balance]         # 引数としてとれる型一覧


# 変換規則の定義
parseRules = {
    NoneType: {},
    Balance: {
        "amount":
            lambda v: v.amount,
        "description":
            lambda v: v.description,
        "category":
            lambda v: v.categoryName,
        "delete":
            lambda v: html_a(
                content="削除する",
                href="/view/balance" + str(v.id) + "/delete/")
    }
}

# デフォルトのフォーマットの定義
# コンマ区切りで要素名を並べる
defaultFormats = {
    NoneType: "",
    Balance: "amount,description,category,delete"
}


# 補助メソッド
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
