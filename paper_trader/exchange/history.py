from dataclasses import dataclass
from datetime import datetime

from paper_trader.utils.price import Price


@dataclass
class PriceTime:
    price: Price
    time: datetime
