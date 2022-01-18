from dataclasses import dataclass
from datetime import datetime
from enum import Enum, auto, unique

from paper_trader.db.decorator import primary_key
from paper_trader.utils.price import Price


@unique
class Side(Enum):
    BUY = auto()
    SELL = auto()


@dataclass
@primary_key("symbol", "placed")
class Order:
    symbol: str
    placed: datetime
    side: Side
    price: Price
    quantity: int
    fee: Price
    filled: int

    @property
    def net_quantity(self):
        return self.quantity if self.side == Side.BUY else -self.quantity


@dataclass
@primary_key("symbol", "filled")
class Fill:
    symbol: str
    filled: datetime
    side: Side
    price: Price
    quantity: int
    fee: Price

    @property
    def net_quantity(self):
        return self.quantity if self.side == Side.BUY else -self.quantity
