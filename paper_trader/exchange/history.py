from dataclasses import dataclass
from datetime import datetime

from paper_trader.utils.dataclasses import primary_key
from paper_trader.utils.price import Price


@dataclass
class PriceTime:
    price: Price
    time: datetime


PriceTimes = list[PriceTime]


@primary_key("symbol", "time")
@dataclass
class SymbolPriceTime:
    symbol: str
    price: Price
    time: datetime


SymbolPriceTimes = list[SymbolPriceTime]
