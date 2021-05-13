from typing import NamedTuple, List

from nhlstats.game.location import Location
from nhlstats.game.shifts import Shift
from nhlstats.time_tracking import GameTime


class Event(NamedTuple):
    """
    An Event is a single play, from one player's perspective, which occurs over the course of a game.

    What that means is that each event which involves multiple players is represented once for each player, e.g:

    A faceoff has a FACEOFF_WIN and a FACEOFF_LOSS event
    a blocked shot has a BLOCKED_SHOT and a BLOCK event
    a goal has a GOAL, ASSIST, and GOAL_AGAINST event
    etc.

    """
    location: Location
    type: str
    team: str
    time: GameTime
    period: str
    player: str
    shifts: List[Shift]

    @classmethod
    def from_raw(cls, data, shifts):
        location = Location(data['x'], data['y'])
        time = GameTime(data['period_time_elapsed'], data['period'])
        players_on_ice = shifts.on_ice_for(time)
        return cls(location, data['event_type'], data['team_for'], time, data['period'], data['player'], players_on_ice)

    @property
    def players_for(self):
        return [s for s in self.shifts if s.team == self.team]

    @property
    def players_against(self):
        return [s for s in self.shifts if s.team != self.team]

    def __repr__(self):
        return '<Event type={} by={} for={} time={}>'.format(self.type, self.player, self.team, self.time)
