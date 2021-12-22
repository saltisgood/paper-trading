from dataclasses import dataclass
from decimal import Decimal
from enum import Enum, auto, unique

from paper_trader.db.converter import register_converter

_QUANTIZE = Decimal("1.0000")


class Price:
    def __init__(self, value: Decimal):
        self._set_value(value)

    def _set_value(self, value: Decimal):
        if type(value) is not Decimal:
            value = Decimal(value)
        value = value.quantize(_QUANTIZE)
        self._value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, v: Decimal):
        self._set_value(v)

    def __eq__(self, other):
        if type(other) is not Price:
            raise NotImplementedError()

        return self._value == other._value

    def __repr__(self):
        return str(self.value)

    def __str__(self):
        return str(self.value)


@register_converter(Decimal)
def decimal_to_db(d=None, db=None):
    if d is not None:
        return str(d)
    assert db is not None
    return Decimal(db)


@register_converter(Price)
def price_to_db(p=None, db=None):
    if p is not None:
        return str(p.value)
    assert db is not None
    return Price(db)


@unique
class Currency(Enum):
    AUD = auto()
    USD = auto()


@dataclass
class PriceCurrency:
    price: Price
    currency: Currency


@dataclass
class PriceQuantity:
    price: Price
    quantity: int
