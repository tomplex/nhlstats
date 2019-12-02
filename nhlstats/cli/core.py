import click

from datetime import date

from nhlstats.apiclient import list_games, list_plays
from nhlstats.cli.helpers import ensure_yyymmdd_date, normalize_game_summary, normalize_event
from nhlstats.cli.output import OutputFormat


@click.group()
def cli():
    pass


@cli.command(name='list-games')
@click.argument('start_date', default=str(date.today()), callback=ensure_yyymmdd_date)
@click.argument('end_date', default=str(date.today()), callback=ensure_yyymmdd_date)
@click.option('--output-format', type=click.Choice(OutputFormat.options()), default='text', callback=OutputFormat.from_click_option)
def _list_games(start_date, end_date, output_format: OutputFormat):
    """
    List all games from START_DATE to END_DATE. Dates should be of the form YYYY-MM-DD. Both date arguments default to
    "today" by system time, so you can omit the final argument to get a range from the first date to today.
    """
    games = list(map(normalize_game_summary, list_games(start_date, end_date)))
    output_format.echo(games)


@cli.command(name='list-plays')
@click.argument('game_id')
@click.option('--output-format', type=click.Choice(OutputFormat.options()), default='text', callback=OutputFormat.from_click_option)
def _list_plays(game_id, output_format: OutputFormat):
    """
    List all play events which occurred in the given GAME_ID.
    """
    plays = list(map(normalize_event, list_plays(game_id)))
    output_format.echo(plays)


@cli.command(name='list-shots')
@click.argument('game_id')
@click.option('--output-format', type=click.Choice(OutputFormat.options()), default='text', callback=OutputFormat.from_click_option)
def _list_shots(game_id, output_format: OutputFormat):
    """
    List all shot events which occurred in the given GAME_ID.
    """
    plays = list(map(normalize_event, list_plays(game_id)))
    plays = list(filter(
        lambda p: 'SHOT' in p['event_type'] or p['event_type'] == 'GOAL', plays
    ))
    output_format.echo(plays)
