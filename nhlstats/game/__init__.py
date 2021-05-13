from nhlstats import list_plays, list_shifts
from nhlstats.game.event import Event
from nhlstats.game.shifts import Shifts, Shift
from nhlstats.time_tracking import TimeDelta
from nhlstats.game.location import Location


class Game:
    """
    A Game contains information about events which occurred in a game and who was on the ice when they happened.
    """

    def __init__(self, gameid):
        self._shifts = Shifts([Shift.from_raw(s) for s in list_shifts(gameid)])
        self._events = [Event.from_raw(e, self._shifts) for e in list_plays(gameid)]

    def __iter__(self):
        return iter(self._events)

    def __len__(self):
        return len(self._events)

    def __getitem__(self, item):
        if isinstance(item, slice):
            if isinstance(item.start, int) or isinstance(item.stop, int):
                raise TypeError
            start = TimeDelta.from_timestamp(item.start) if item.start else TimeDelta(seconds=0)
            stop = TimeDelta.from_timestamp(item.stop) if item.stop else TimeDelta(seconds=60*65)
            return list(filter(lambda e: e.time.between(start, stop), self._events))
        return self._events[item]

    @property
    def shifts(self):
        return self._shifts
