import json

import click
import tabulate

from enum import Enum

from nhlstats.cli.helpers import list_of_dicts_to_csv


class OutputFormat(Enum):
    TEXT = 'text'
    CSV = 'csv'
    JSON = 'json'
    POSTGRES = 'postgres'

    @staticmethod
    def options():
        return list(out.value for out in OutputFormat)

    @classmethod
    def from_click_option(cls, ctx, param, value):
        try:
            return cls(value)
        except:
            raise click.BadParameter(value)

    def echo(self, events: list) -> None:
        if self.value == 'text':
            click.echo(tabulate.tabulate(events, headers='keys'))

        elif self.value == 'csv':
            click.echo(list_of_dicts_to_csv(events))

        elif self.value == 'json':
            click.echo(json.dumps({'plays': events}))

        else:
            raise click.UsageError("Output format {} is not implemented.".format(self.value))
