from decimal import Decimal

class Price:
    def __init__(self, value: Decimal):
        self._value = value
    
    @property
    def value(self): return self._value

    @value.setter
    def value(self, v: Decimal):
        self._value = v

class Currency:
    def __init__(self, name: str):
        self._name = name
    
    @property
    def name(self):
        return self._name

class PriceCurrency:
    def __init__(self, price: Price, currency: Currency):
        self._price = price
        self._currency = currency
    
    @property
    def price(self):
        return self._price

    @property
    def currency(self):
        return self._currency