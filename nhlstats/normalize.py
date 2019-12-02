__author__ = 'tcaruso'


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


def event(ev):
    e = {
        'datetime': ev['about']['dateTime'],
        'period': ev['about']['period'],
        'period_time': ev['about']['periodTime'],
        'period_time_remaining': ev['about']['periodTimeRemaining'],
        'period_type': ev['about']['periodType'],
        'x': ev.get('coordinates', {}).get('x'),
        'y': ev.get('coordinates', {}).get('y'),
        'event_type': ev['result']['eventTypeId'],
        'event_secondary_type': ev['result'].get('secondaryType'),
        'event_description': ev['result'].get('description'),
        'team_for': ev.get('team', {}).get('triCode'),
    }

    for idx, player in enumerate(ev.get('players', [])):
        e['player_{}'.format(idx + 1)] = player.get('player', {}).get('fullName')
        e['player_{}_type'.format(idx + 1)] = player.get('playerType')
        e['player_{}_id'.format(idx + 1)] = player.get('player', {}).get('id')

    return e