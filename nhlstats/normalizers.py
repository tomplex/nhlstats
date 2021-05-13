__author__ = "tcaruso"


import math

from nhlstats.constants import FENWICK_EVENTS, SHOT_EVENTS, CORSI_EVENTS, NET_X_LOCATION


def game_summary(gs):
    return {
        "date": gs["gameDate"][:10],
        "game_id": gs["gamePk"],
        "home_team": gs["teams"]["home"]["team"]["name"],
        "home_score": gs["teams"]["home"]["score"],
        "away_team": gs["teams"]["away"]["team"]["name"],
        "away_score": gs["teams"]["away"]["score"],
        "season": gs["season"],
        "game_state": gs["status"]["detailedState"],
    }


def _calculate_distance(e):
    try:
        delta_x = NET_X_LOCATION - abs(int(e["x"]))
        delta_y = -1 * int(e["y"])
        return math.sqrt(delta_x ** 2 + delta_y ** 2)
    except Exception as e:
        return None


def _calculate_angle(e):
    try:
        return abs(math.atan(e["y"] / (NET_X_LOCATION - abs(e["x"]))) * (180 / math.pi))
    except:
        return None


EVENT_TYPE_MAP = {
    ("GOAL", "Scorer"): "GOAL",
    ("GOAL", "Assist"): "ASSIST",
    ("GOAL", "Goalie"): "GOAL_AGAINST",
    ("SHOT", "Shooter"): "SHOT",
    ("SHOT", "Goalie"): "SAVE",
    ("HIT", "Hitter"): "HIT",
    ("HIT", "Hittee"): "HITTEE",
    ("BLOCKED_SHOT", "Blocker"): "BLOCK",
    ("BLOCKED_SHOT", "Shooter"): "BLOCKED_SHOT",
    ("MISSED_SHOT", "Shooter"): "MISSED_SHOT",
    ("GIVEAWAY", "PlayerID"): "GIVEAWAY",
    ("TAKEAWAY", "PlayerID"): "TAKEAWAY",
    ("FACEOFF", "Winner"): "FACEOFF_WIN",
    ("FACEOFF", "Loser"): "FACEOFF_LOSS",
    ("PENALTY", "PenaltyOn"): "PENALTY_ON",
    ("PENALTY", "DrewBy"): "PENALTY_DRAWN",
}


def get_event_type(initial_type, player):
    key = (initial_type, player.get('playerType'))
    if None in key:
        return initial_type

    try:
        return EVENT_TYPE_MAP[key]
    except Exception as e:
        raise Exception("no match for event {} with key {}".format(e, repr(key)))


def should_switch_team(event_type):
    return event_type in (
        "GOAL_AGAINST", "SAVE", "BLOCKED_SHOT", "FACEOFF_LOSS", "PENALTY_DRAWN", "HITTEE"
    )


def other_team(team: str, teams: tuple):
    return teams[len(teams) - (teams.index(team) + 1)]


def normalize_event(ev, teams):
    initial_event_type = ev["result"]["eventTypeId"]
    players = ev.get("players", [{}])

    for player in players:
        new_event_type = get_event_type(initial_event_type, player)

        e = {
            "event_id": ev["about"]["eventIdx"],
            "datetime": ev["about"]["dateTime"],
            "period": ev["about"]["period"],
            "period_time_elapsed": ev["about"]["periodTime"],
            "period_time_remaining": ev["about"]["periodTimeRemaining"],
            "regulation_time_remaining": "",
            "period_type": ev["about"]["periodType"],
            "x": ev.get("coordinates", {}).get("x"),
            "y": ev.get("coordinates", {}).get("y"),
            "event_type": new_event_type,
            "event_secondary_type": ev["result"].get("secondaryType"),
            "team_for": ev.get("team", {}).get("triCode"),
            "player": player.get("player", {}).get("fullName"),
            "player_type": player.get("playerType"),
            "player_id": player.get("player", {}).get("id"),
        }

        if new_event_type == "STOP":
            e["event_secondary_type"] = ev["result"].get("description")

        e["is_shot"] = new_event_type in SHOT_EVENTS
        e["is_corsi"] = new_event_type in CORSI_EVENTS
        e["is_fenwick"] = new_event_type in FENWICK_EVENTS

        e["shot_distance"] = _calculate_distance(e) if new_event_type in ("SHOT", "SAVE", "GOAL") else None
        e["shot_angle"] = _calculate_angle(e) if new_event_type in ("SHOT", "SAVE", "GOAL") else None

        if should_switch_team(new_event_type):
            e['team_for'] = other_team(e['team_for'], teams)

        yield e


def normalize_events(evs, teams):
    for event in evs:
        for fanout_event in normalize_event(event, teams):
            yield fanout_event


def normalize_shift(sh):
    return {
        "id": sh["id"],
        "first_name": sh["firstName"],
        "last_name": sh["lastName"],
        "period": sh["period"],
        "shift_number": sh["shiftNumber"],
        "start_time": sh["startTime"],
        "end_time": sh["endTime"],
        "duration": sh["duration"],
        "team_abbreviation": sh["teamAbbrev"],
        "event_description": sh["eventDescription"],
        "event_details": sh["eventDetails"],
        "event_number": sh["eventNumber"],
    }
