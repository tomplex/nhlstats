
import re

import click


def ensure_yyymmdd_date(ctx, param, value):
    match = re.search(r'\d\d\d\d-\d\d-\d\d', value)

    if match is None:
        raise click.BadParameter("Date must be of the form YYYY-MM-DD.")

    return value


def normalize_game_summary(gs):
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


def normalize_event(event):
    e = {
        'datetime': event['about']['dateTime'],
        'period': event['about']['period'],
        'period_time': event['about']['periodTime'],
        'period_time_remaining': event['about']['periodTimeRemaining'],
        'period_type': event['about']['periodType'],
        'x': event.get('coordinates', {}).get('x'),
        'y': event.get('coordinates', {}).get('y'),
        'event_type': event['result']['eventTypeId'],
        'event_secondary_type': event['result'].get('secondaryType'),
        'event_description': event['result'].get('description'),
        'team_for': event.get('team', {}).get('triCode'),
    }

    for idx, player in enumerate(event.get('players', [])):
        e['player_{}'.format(idx + 1)] = player.get('player', {}).get('fullName')
        e['player_{}_type'.format(idx + 1)] = player.get('playerType')
        e['player_{}_id'.format(idx + 1)] = player.get('player', {}).get('id')

    return e


def list_of_dicts_to_csv(ld):
    return ','.join(ld[0].keys()) + '\n' + \
           '\n'.join(','.join(str(val) if (val or val == 0) else '' for val in row.values()) for row in ld)
