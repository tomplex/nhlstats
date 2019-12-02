__author__ = 'tcaruso'

import re

import click


def ensure_yyymmdd_date(ctx, param, value):
    match = re.search(r'\d\d\d\d-\d\d-\d\d', value)

    if match is None:
        raise click.BadParameter("Date must be of the form YYYY-MM-DD.")

    return value

