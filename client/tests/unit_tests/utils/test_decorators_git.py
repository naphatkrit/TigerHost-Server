import click
import pytest

from click_extensions.decorators import print_markers

from tigerhost.utils import decorators


@click.command()
@decorators.store_vcs
@click.pass_context
@print_markers
def command_with_context(ctx):
    vcs = ctx.obj['vcs']
    if vcs is None:
        click.echo('no git')
    else:
        click.echo('has git')


@pytest.mark.parametrize('command,exit_code', [
    (command_with_context, 0),
])
def test_no_git(runner, command, exit_code):
    result = runner.invoke(command)
    assert result.exit_code == exit_code
    assert 'no git' in result.output


@pytest.mark.parametrize('command,exit_code', [
    (command_with_context, 0),
])
def test_has_git(runner, make_git_repo, command, exit_code):
    result = runner.invoke(command)
    assert result.exit_code == exit_code
    assert 'has git' in result.output
