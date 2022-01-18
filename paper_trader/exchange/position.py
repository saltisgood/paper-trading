from .orders import Fill

Fills = list[Fill]


class Position:
    def __init__(self):
        self._fills = Fills()

    @property
    def fills(self):
        return self._fills

    @property
    def net_quantity(self):
        return sum(f.net_quantity for f in self._fills)

    @property
    def net_profit(self):
        return sum(((-f.net_quantity * f.price) - f.fee) for f in self._fills)


Symbol = str
Positions = dict[Symbol, Position]


class TotalPositions:
    def __init__(self):
        self._positions = Positions()

    @property
    def positions(self):
        return self._positions
