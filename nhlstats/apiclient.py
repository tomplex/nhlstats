import datetime

import requests

BASE_URL = "https://statsapi.web.nhl.com"
SCHEDULE_URL = BASE_URL + "/api/v1/schedule"
LIVE_PLAYS_URL = BASE_URL + "/api/v1/game/{game_id}/feed/live"


def list_games(start_date=None, end_date=None):
    """

    Args:
        start_date:
        end_date:

    Returns:

    """
    if start_date is None:
        start_date = str(datetime.date.today())
    if end_date is None:
        end_date = str(datetime.date.today())

    resp = requests.get(SCHEDULE_URL, params={'startDate': start_date, 'endDate': end_date})

    data = resp.json()

    games = [
        game for date in data['dates'] for game in date['games']
    ]

    return games


def list_plays(game_id):
    resp = requests.get(LIVE_PLAYS_URL.format(game_id=game_id))

    data = resp.json()

    if data.get('message'):
        return

    return data['liveData']['plays']['allPlays']
