__author__ = "tcaruso"

from datetime import timedelta


from nhlstats.constants import FULL_GAME, ONE_PERIOD


def _shave_seconds(seconds):
    """Recursive implementation - not safe for large values."""
    if seconds >= 60:
        mins, seconds = _shave_seconds(seconds - 60)
        return mins + 1, seconds
    else:
        return 0, seconds


# helper functions for "between" functionality, essentially a matrix which maps inclusivity to functions
# for gt/lt expressions
_between_map = {
    (True, True): lambda t, start, stop: start <= t <= stop,
    (True, False): lambda t, start, stop: start <= t < stop,
    (False, True): lambda t, start, stop: start < t <= stop,
    (False, False): lambda t, start, stop: start < t < stop,
}


class TimeDelta(timedelta):
    @property
    def minutes(self):
        return _shave_seconds(self.total_seconds())[0]

    def __str__(self):
        return '{}:{:02}'.format(self.minutes, self.seconds - (60 * self.minutes))

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        if isinstance(other, str):
            return str(self) == other
        elif isinstance(other, TimeDelta):
            return super().__eq__(other)
        raise TypeError

    @classmethod
    def from_timestamp(cls, ts):
        event_time_mins, event_time_secs = map(int, ts.split(':'))
        return cls(minutes=event_time_mins, seconds=event_time_secs)

    def between(self, start, stop, inclusive_start=True, inclusive_stop=False):
        return _between_map[inclusive_start, inclusive_stop](self, start, stop)


class GameTime:
    def __init__(self, t, period):
        self.period = int(period)
        self.period_timedelta = TimeDelta.from_timestamp(t)

        total_seconds = ((ONE_PERIOD * (int(self.period) - 1)) + self.period_timedelta).total_seconds()
        self.timedelta = TimeDelta(seconds=total_seconds)
        self.time_mins = self.timedelta.minutes
        self.time_secs = self.timedelta.seconds

    def __gt__(self, other):
        return self.timedelta > other

    def __lt__(self, other):
        return self.timedelta < other

    def __ge__(self, other):
        return self.timedelta >= other

    def __le__(self, other):
        return self.timedelta <= other

    def __eq__(self, other):
        if isinstance(other, str):
            return str(self) == other
        elif isinstance(other, GameTime):
            return self.total_time_elapsed == other.total_time_elapsed
        elif isinstance(other, TimeDelta):
            return self.total_time_elapsed == other
        raise TypeError

    def __str__(self):
        return str(self.timedelta)

    def __repr__(self):
        return '<EventTime time={} period={} tte={}>'.format(self.timedelta, self.period, self.total_time_elapsed)

    @property
    def total_time_elapsed(self):
        seconds = ((ONE_PERIOD * (int(self.period) - 1)) + self.timedelta).total_seconds()
        return TimeDelta(seconds=seconds)

    @property
    def period_time_elapsed(self):
        return self.timedelta

    @property
    def regulation_time_remaining(self):
        return 0 if self > FULL_GAME else TimeDelta(seconds=(FULL_GAME - self.timedelta).seconds)

    def between(self, start, stop, inclusive_start=True, inclusive_stop=False):
        return self.timedelta.between(start, stop, inclusive_start, inclusive_stop)
