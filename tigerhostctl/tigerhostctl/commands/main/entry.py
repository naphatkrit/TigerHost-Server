import click

from tigerhostctl.commands.main.create import create
from tigerhostctl.commands.main.destroy import destroy


CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.group(context_settings=CONTEXT_SETTINGS)
def entry():
    pass


entry.add_command(create)
entry.add_command(destroy)
