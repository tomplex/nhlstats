__author__ = 'tcaruso'

import importlib

import click

from enum import Enum


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
        try:
            formatter = importlib.import_module('nhlstats.formatters.{}'.format(self.value))
            click.echo(formatter.dumps(events))
        except:
            raise click.UsageError("Output format {} is not implemented.".format(self.value))
