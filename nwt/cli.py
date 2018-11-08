# -*- coding: utf-8 -*-
"""
Console script for nwt.
"""

import os
import sys
import click

from nwt import __version__
from nwt.cmd import Interactive
from nwt.setup.install import install as setup


@click.group(invoke_without_command=True)
@click.pass_context
@click.version_option()
def main(ctx):
    """
    Bible new world translation in cli
    """

    if not ctx.invoked_subcommand:
        greet()
        session = Interactive()
        session.run()


def greet():
    """
    Print greeting in terminal
    """

    width = os.get_terminal_size()[0]
    s_version = 'Version: ' + __version__
    title = 'bible new world translation'

    print('-' * width)
    print()
    print(title.center(width))
    print(s_version.center(width))
    print()
    print('-' * width)


@main.command()
def download():
    pass


@main.command()
@click.argument('file_path')
def install(file_path):
    setup(file_path)


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
