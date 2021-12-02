from .orders import Fill

Fills = list[Fill]

class Position:
    def __init__(self):
        self._fills = Fills()
    
    @property
    def net_quantity(self):
        return sum(f.net_quantity for f in self._fills)

ItemKey = str
Positions = dict[ItemKey, Position]

class TotalPositions:
    def __init__(self):
        self._positions = Positions()