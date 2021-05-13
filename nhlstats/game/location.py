import math
from typing import NamedTuple

from nhlstats.constants import NET_X_LOCATION


class Location(NamedTuple):
    """
    A Location is a pair of x,y coordinates on the rink.
    """
    x: int
    y: int

    @property
    def angle(self):
        try:
            return abs(math.atan(self.y / (NET_X_LOCATION - abs(self.x))) * (180 / math.pi))
        except:
            return None

    @property
    def distance(self):
        try:
            delta_x = NET_X_LOCATION - abs(int(self.x))
            delta_y = -1 * int(self.y)
            return math.sqrt(delta_x ** 2 + delta_y ** 2)
        except Exception as e:
            return None