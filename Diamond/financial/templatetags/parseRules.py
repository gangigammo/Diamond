from typing import Union
from financial.models import Balance
from .util import *

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
                contents="削除する",
                href="/view/balance" + str(v.id) + "/delete/")
    }
}

# デフォルトのフォーマットの定義
# コンマ区切りで要素名を並べる
defaultFormats = {
    NoneType: "",
    Balance: "amount,description,category,delete"
}
