__author__ = 'tcaruso'


import math

from nhlstats.constants import FENWICK_EVENTS, SHOT_EVENTS, CORSI_EVENTS

NET_X_LOCATION = 89


def game_summary(gs):
    return {
        'date': gs['gameDate'][:10],
        'game_id': gs['gamePk'],
        'home_team': gs['teams']['home']['team']['name'],
        'home_score': gs['teams']['home']['score'],
        'away_team': gs['teams']['away']['team']['name'],
        'away_score': gs['teams']['away']['score'],
        'season': gs['season'],
        'game_state': gs['status']['detailedState'],
    }


def _calculate_distance(e):
    try:
        delta_x = NET_X_LOCATION - abs(int(e['x']))
        delta_y = -1 * int(e['y'])
        return math.sqrt(delta_x ** 2 + delta_y ** 2)
    except Exception as e:
        return None


def _calculate_angle(e):
    try:
        return abs(math.atan(e['y'] / (NET_X_LOCATION - abs(e['x']))) * (180 / math.pi))
    except:
        return None


def event(ev, max_players=1):
    event_type = ev['result']['eventTypeId']
    e = {
        'datetime': ev['about']['dateTime'],
        'period': ev['about']['period'],
        'period_time': ev['about']['periodTime'],
        'period_time_remaining': ev['about']['periodTimeRemaining'],
        'period_type': ev['about']['periodType'],
        'x': ev.get('coordinates', {}).get('x'),
        'y': ev.get('coordinates', {}).get('y'),
        'event_type': event_type,
        'event_secondary_type': ev['result'].get('secondaryType'),
        'event_description': ev['result'].get('description'),
        'is_shot': event_type in SHOT_EVENTS,
        'is_corsi': event_type in CORSI_EVENTS,
        'is_fenwick': event_type in FENWICK_EVENTS,
        'team_for': ev.get('team', {}).get('triCode')
    }

    e['shot_distance'] = _calculate_distance(e) if e['is_corsi'] else None
    e['shot_angle'] = _calculate_angle(e) if e['is_corsi'] else None

    players = ev.get('players', [])
    if len(players) < max_players:
        players.extend([{}] * (max_players - len(players)))

    for idx, player in enumerate(players):
        e['player_{}'.format(idx + 1)] = player.get('player', {}).get('fullName')
        e['player_{}_type'.format(idx + 1)] = player.get('playerType')
        e['player_{}_id'.format(idx + 1)] = player.get('player', {}).get('id')

    return e


def events(evs):
    max_players = max(len(e.get('players', [])) for e in evs)

    return [event(ev, max_players) for ev in evs]


def shift(sh):
    return {
        'id': sh['id'],
        'first_name': sh['firstName'],
        'last_name': sh['lastName'],
        'period': sh['period'],
        'shift_number': sh['shiftNumber'],
        'start_time': sh['startTime'],
        'end_time': sh['endTime'],
        'duration': sh['duration'],
        'team_abbreviation': sh['teamAbbrev'],
        'event_description': sh['eventDescription'],
        'event_details': sh['eventDetails'],
        'event_number': sh['eventNumber']
    }