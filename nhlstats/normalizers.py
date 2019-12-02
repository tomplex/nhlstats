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


def event(ev, max_players=1):
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
