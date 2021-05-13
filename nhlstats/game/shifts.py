from typing import NamedTuple

from nhlstats.time_tracking import TimeDelta, GameTime


class Shifts:
    def __init__(self, shifts):
        self._shifts = shifts

    def __len__(self):
        return len(self._shifts)

    def __getitem__(self, item):
        if isinstance(item, slice):
            if isinstance(item.start, int) or isinstance(item.stop, int):
                raise TypeError

            if item.stop is None:
                stop = TimeDelta(seconds=60*65)
            elif not isinstance(item.stop, TimeDelta):
                stop = TimeDelta.from_timestamp(item.stop)
            else:
                stop = item.stop

            if not isinstance(item.start, TimeDelta):
                start = TimeDelta.from_timestamp(item.start) if item.start else TimeDelta(seconds=0)
            else:
                start = item.start

            return list(filter(lambda e: e.time.between(start, stop), self._shifts))
        elif isinstance(item, int):
            return self._shifts[item]
        elif isinstance(item, str):
            item = TimeDelta.from_timestamp(item)
        elif isinstance(item, GameTime):
            pass

        return list(filter(lambda e: e.time == item, self._shifts))

    def on_ice_for(self, time: TimeDelta):
        def filter_shifts(s: Shift):
            return time.between(s.start, s.end)

        return list(filter(filter_shifts, self._shifts))


class Shift(NamedTuple):
    start: GameTime
    end: GameTime
    player: str
    period: int
    shift_number: int
    duration: int
    team: str

    @classmethod
    def from_raw(cls, data):
        period = data['period']
        start_time = GameTime(data['start_time'], period)
        end_time = GameTime(data['end_time'], period)
        player = '{} {}'.format(data['first_name'], data['last_name'])
        return cls(start_time, end_time, player, period, data['shift_number'], data['duration'], data['team_abbreviation'])

    def __repr__(self):
        return "<Shift player={} start={} end={} team={}>".format(self.player, self.start, self.end, self.team)
