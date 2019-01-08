from django.template.defaultfilters import register
from financial.models import Balance
from typing import Optional


@register.filter
def balanceToRow(value: Balance) -> str:
    return str(value.amount) + str(value.description) + str(value.categoryName)
