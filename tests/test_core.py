# -*- coding: utf-8 -*-

"""
Module to test functionality of the click ``did-you-mean`` extension.
"""

import pytest
import click
from click.testing import CliRunner
from click_didyoumean import DYMGroup, DYMCommandCollection


@pytest.fixture(scope="function")
def runner(request):
    return CliRunner()


def test_basic_functionality_with_group(runner):
    @click.group(cls=DYMGroup)
    def cli():
        pass

    @cli.command()
    def foo():
        pass

    @cli.command()
    def bar():
        pass

    @cli.command()
    def barrr():
        pass

    result = runner.invoke(cli, ["barr"])
    assert result.output == (
        "Usage: cli [OPTIONS] COMMAND [ARGS]...\n\n"
        "Error: No such command \"barr\".\n\n"
        "Did you mean one of these?\n"
        "    barrr\n"
        "    bar\n"
    )


def test_basic_functionality_with_commandcollection(runner):
    @click.group()
    def cli1():
        pass

    @cli1.command()
    def foo():
        pass

    @cli1.command()
    def bar():
        pass

    @click.group()
    def cli2():
        pass

    @cli2.command()
    def barrr():
        pass

    cli = DYMCommandCollection(sources=[cli1, cli2])
    result = runner.invoke(cli, ["barr"])
    assert result.output == (
        "Usage: root [OPTIONS] COMMAND [ARGS]...\n\n"
        "Error: No such command \"barr\".\n\n"
        "Did you mean one of these?\n"
        "    barrr\n"
        "    bar\n"
    )


def test_cutoff_factor(runner):
    @click.group(cls=DYMGroup, max_suggestions=3, cutoff=1.0)
    def cli():
        pass

    @cli.command()
    def foo():
        pass

    @cli.command()
    def bar():
        pass

    @cli.command()
    def barrr():
        pass

    # if cutoff factor is 1.0 the match must be perfect.
    result = runner.invoke(cli, ["barr"])
    assert result.output == (
        "Usage: cli [OPTIONS] COMMAND [ARGS]...\n\n"
        "Error: No such command \"barr\".\n"
    )


def test_max_suggetions(runner):
    @click.group(cls=DYMGroup, max_suggestions=2, cutoff=0.5)
    def cli():
        pass

    @cli.command()
    def foo():
        pass

    @cli.command()
    def bar():
        pass

    @cli.command()
    def barrr():
        pass

    @cli.command()
    def baarr():
        pass

    # if cutoff factor is 1.0 the match must be perfect.
    result = runner.invoke(cli, ["barr"])
    assert result.output == (
        "Usage: cli [OPTIONS] COMMAND [ARGS]...\n\n"
        "Error: No such command \"barr\".\n\n"
        "Did you mean one of these?\n"
        "    barrr\n"
        "    baarr\n"
    )
