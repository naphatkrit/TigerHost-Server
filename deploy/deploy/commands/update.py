import click
import subprocess32 as subprocess

from tigerhost.utils.decorators import print_markers

from deploy import settings
from deploy.utils.decorators import ensure_project_path, require_docker_machine


@click.command()
@print_markers
@ensure_project_path
@require_docker_machine
def update():
    subprocess.check_call([settings.APP_NAME, 'addons', 'update'])
    subprocess.check_call([settings.APP_NAME, 'addons', 'copy-credentials'])
    subprocess.check_call([settings.APP_NAME, 'main', 'update'])