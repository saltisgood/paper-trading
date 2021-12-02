from datetime import datetime
from enum import Enum, auto, unique
import sqlite3

from paper_trader.utils.price import Price

@unique
class Side(Enum):
    BUY = auto()
    SELL = auto()

class _BaseOrder:
    def __init__(self, side: Side, price: Price, quantity: int, placed: datetime = None):
        self._side = side
        self._price = price
        self._quantity = quantity
        self._placed = placed
    
    @property
    def side(self):
        return self._side
    
    @property
    def price(self):
        return self._price

    @property
    def quantity(self):
        return self._quantity
    
    @property
    def net_quantity(self):
        return self.quantity if self.side == Side.BUY else -self.quantity
    
    @property
    def placed(self):
        return self._placed
    
class Order(_BaseOrder):
    def __init__(self, *nargs, **kwargs):
        super().__init__(*nargs, **kwargs)

    def __conform__(self, protocol):
        if protocol == sqlite3.PrepareProtocol:
            return f'{self.side};{self.price.value};{self.quantity}'

class Fill(_BaseOrder):
    def __init__(self, filled: datetime = None, *nargs, **kwargs):
        super().__init__(*nargs, **kwargs)
        self._filled = filled
    
    @property
    def filled(self):
        return self._filled