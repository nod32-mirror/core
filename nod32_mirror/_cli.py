"""
# todo
"""

import click


@click.group()
def cli():
    """
    Command line interface for nod32_mirror.
    """


@cli.command("update", help="Update current versions")
def update():
    """
    Update current versions
    """
    print("Update action")


@cli.command("current", help="Show current versions")
def current():
    """
    Show current versions
    """
    print("Current action")


@cli.command("check", help="Check updates for current versions")
def check():
    """
    Check updates for current versions
    """
    print("Check action")
