from django.utils.safestring import SafeText, mark_safe
from typing import Union
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
            lambda v: mark_safe("<a href=\"/view/balance" +
                                str(v.id)+"/delete/\">削除</a>")
    }
}

# デフォルトのフォーマットの定義
# コンマ区切りで要素名を並べる
defaultFormats = {
    NoneType: "",
    Balance: "amount,description,category,delete"
}
