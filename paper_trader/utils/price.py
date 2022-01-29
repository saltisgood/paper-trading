from dataclasses import dataclass
from decimal import Decimal
from enum import Enum, auto, unique
from functools import total_ordering

from paper_trader.db.converter import register_converter

_QUANTIZE = Decimal("1.0000")


@total_ordering
class Price:
    def __init__(self, value: Decimal | str | float):
        self._set_value(value)

    def _set_value(self, value: Decimal | str | float):
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

    def __lt__(self, other):
        if type(other) is not Price:
            raise NotImplementedError()

        return self._value < other._value

    def __add__(self, other):
        if type(other) is not Price:
            raise NotImplementedError()

        return Price(self._value + other._value)

    def __sub__(self, other):
        if type(other) is not Price:
            raise NotImplementedError()

        return Price(self._value - other._value)

    def __truediv__(self, other):
        if not isinstance(other, Price):
            raise NotImplementedError()

        return self._value / other._value

    def __mul__(self, other):
        if isinstance(other, int) or isinstance(other, Decimal):
            return Price(self._value * other)
        return Price(self._value * other._value)

    def __rmul__(self, other):
        return self * other

    def __repr__(self):
        return str(self.value)

    def __str__(self):
        return str(self.value)


@register_converter(Decimal)
class DecimalConverter:
    @staticmethod
    def from_db(value: str) -> Decimal:
        return Decimal(value)

    @staticmethod
    def to_db(value: Decimal) -> str:
        return str(value)


@register_converter(Price)
class PriceConverter:
    @staticmethod
    def from_db(value: str) -> Price:
        return Price(Decimal(value))

    @staticmethod
    def to_db(value: Price) -> str:
        return str(value.value)


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
