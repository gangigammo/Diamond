from django.template.defaultfilters import register
from financial.models import Balance
from typing import Optional


@register.filter
def balanceToRow(value: Balance) -> str:
    if not(type(value) in (Balance, type(None))):
        raise TypeError("toRowフィルタに渡す値の型が違います")
    string = value and str(value.amount) + \
        str(value.description) + str(value.categoryName)
    string = string or "none"
    return string
