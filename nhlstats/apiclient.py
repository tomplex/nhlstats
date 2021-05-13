__author__ = "tcaruso"

import datetime

import requests

from nhlstats import normalizers


BASE_URL = "https://statsapi.web.nhl.com"
SCHEDULE_URL = BASE_URL + "/api/v1/schedule"
LIVE_PLAYS_URL = BASE_URL + "/api/v1/game/{game_id}/feed/live"

SHIFT_BASE_URL = "https://api.nhle.com/stats/rest/en/shiftcharts"
SHIFT_TEMPLATE = SHIFT_BASE_URL + "?cayenneExp=gameId={game_id}"


def list_games(start_date=None, end_date=None):
    """
    List all games between start_date and end_date. Dates must be in YYYY-MM-DD format.
    If a date is not specified, it will default to "today".

    Args:
        start_date:
        end_date:

    Returns:

    """
    if start_date is None:
        start_date = str(datetime.date.today())
    if end_date is None:
        end_date = str(datetime.date.today())

    resp = requests.get(
        SCHEDULE_URL, params={"startDate": start_date, "endDate": end_date}
    )

    data = resp.json()

    return [
        normalizers.game_summary(game)
        for date in data["dates"]
        for game in date["games"]
    ]


def list_plays(game_id, normalize=True):
    """
    Return normalized play dictionaries.

    Args:
        game_id:
        normalize:

    Returns:

    """
    resp = requests.get(LIVE_PLAYS_URL.format(game_id=game_id))

    data = resp.json()

    if data.get("message"):
        raise Exception("Invalid GAME_ID.")

    plays = data["liveData"]["plays"]["allPlays"]
    teams = (data["gameData"]['teams']['away']['triCode'], data["gameData"]['teams']['home']['triCode'])

    if normalize:
        return normalizers.normalize_events(plays, teams)

    return plays


def list_shots(game_id):
    """
    Return all plays which are some variant of shot: SHOT, MISSED_SHOT, BLOCKED_SHOT, GOAL.

    Args:
        game_id:

    Returns:

    """
    plays = list_plays(game_id)

    return list(
        filter(lambda p: "SHOT" in p["event_type"] or p["event_type"] == "GOAL", plays)
    )


def list_shifts(game_id):
    """
    Return all shifts which occurred in the game.

    Args:
        game_id:

    Returns:

    """
    resp = requests.get(SHIFT_TEMPLATE.format(game_id=game_id))

    data = resp.json()

    return [normalizers.normalize_shift(d) for d in data["data"]]
