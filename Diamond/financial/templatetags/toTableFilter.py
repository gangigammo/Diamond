from django.template.defaultfilters import register
from financial.models import Balance
from typing import Union
from typing import Optional
from typing import List
from typing import Any
import inspect

# HTMLコード
# テーブルの行要素
rowPrefix = "<td>"
rowSuffix = "</td>"


# 型の定義
NoneType = type(None)               # nullを表す
DomainType = Union[Balance]         # 引数としてとれる型一覧


# 変換規則の定義
__mapDicts = {
    NoneType: {},
    Balance: {
        "amount":
            lambda v: v.amount,
        "description":
            lambda v: v.description,
        "category":
            lambda v: v.categoryName
    }
}

# デフォルトのフォーマットの定義
# コンマ区切りで要素名を並べる
__defaultFormats = {
    NoneType: "",
    Balance: "amount,description,category"
}


# 値 -> HTMLテーブルの行要素 への変換 (なければNoneを返す)
@register.filter
def toRow(value: Optional[DomainType], format=None) -> Optional[str]:
    values = value and __parse(value, format)
    string = values and __buildString(
        values=values, prefix=rowPrefix, suffix=rowSuffix)
    return string


@register.filter
def toTable(values: List[DomainType], format=None):
    return "<tr>" + ''.join([toRow(v, format) for v in values]) + "</tr>"

# 値 -> フォーマット通りの順で要素を並べたリスト への変換


def __parse(value: DomainType, format: Optional[str]) -> List[str]:
    # valueの型
    valueType = type(value)
    # valueTypeに対応する変換規則
    mapDict = __mapDicts.get(valueType)
    if mapDict is None:
        caller = inspect.stack()[1][3]
        raise TypeError("型" + str(valueType) + "は" + caller + "の引数として不適切です")
    # formatが与えられてなければ代わりにデフォルトのを使う
    format = format or __defaultFormats.get(valueType)
    if format is None:
        raise SyntaxError("型" + str(valueType) + "のためのformatがありません")
    # コンマ区切りのformatをリスト形式へ変換
    keys = format.split(",")

    def getValue(key):  # keyをvalueに変換するクロージャ
        m = mapDict.get(key)
        if m is None:
            raise SyntaxError("フォーマット" + format + "の内、" + key + "が正しくありません")
        return m(value)
    # formatに沿ってvalueから値を取り出し並べる
    values = [getValue(k) for k in keys]
    return values


# リスト -> 連結した文字列 への変換
def __buildString(values: List[Any], prefix: str, suffix: str) -> str:
    strs = map(str, values)
    string = prefix + (suffix + prefix).join(strs) + suffix
    return string
