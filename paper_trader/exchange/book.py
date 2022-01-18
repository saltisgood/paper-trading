from .orders import Order
from .position import TotalPositions

Orders = list[Order]


class Book:
    def __init__(self, name: str):
        self._name = name
        self._active_orders = Orders()
        self._positions = TotalPositions()

    @property
    def name(self):
        return self._name

    @property
    def active_orders(self):
        return self._active_orders

    @property
    def positions(self):
        return self._positions
