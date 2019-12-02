__author__ = 'tcaruso'

import click

from datetime import date

from nhlstats.apiclient import list_games, list_plays, list_shots
from nhlstats.cli.helpers import ensure_yyymmdd_date
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
    output_format.echo(list_games(start_date, end_date))


@cli.command(name='list-plays')
@click.argument('game_id')
@click.option('--output-format', type=click.Choice(OutputFormat.options()), default='text', callback=OutputFormat.from_click_option)
def _list_plays(game_id, output_format: OutputFormat):
    """
    List all play events which occurred in the given GAME_ID.
    """
    output_format.echo(list_plays(game_id))


@cli.command(name='list-shots')
@click.argument('game_id')
@click.option('--output-format', type=click.Choice(OutputFormat.options()), default='text', callback=OutputFormat.from_click_option)
def _list_shots(game_id, output_format: OutputFormat):
    """
    List all shot events which occurred in the given GAME_ID.
    """
    output_format.echo(list_shots(game_id))
