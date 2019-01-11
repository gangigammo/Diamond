from typing import Union
from financial.models import Balance
from .util import *

# 型の定義
NoneType = type(None)               # nullを表す
DomainType = Union[Balance]         # 引数としてとれる型一覧


# 変換規則の定義
parseRules = {
    NoneType: {
        "none":
            lambda v: "none"
    },
    Balance: {
        "amount":
            lambda v: html_font(("+", v.amount), color="green")
            if v.isIncome else html_font(-v.amount, color="red"),
        "description":
            lambda v: v.description,
        "category":
            lambda v: v.categoryName,
        "delete":
            lambda v: html_a("削除する",
                             href="/view/balance" + str(v.id) + "/delete/"),
        "checkbox":
            lambda v: html_input("", name="balance_select",
                                 type="checkbox", value=str(v.id))
    }
}

# デフォルトのフォーマットの定義
# コンマ区切りで要素名を並べる
defaultFormats = {
    NoneType: "none",
    Balance: "amount,description,category,delete"
}
