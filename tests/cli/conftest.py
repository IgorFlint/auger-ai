import logging

import pytest
from click.testing import CliRunner


@pytest.fixture
def runner():
    return CliRunner()


@pytest.fixture(scope="function")
def isolated(runner):
    with runner.isolated_filesystem():
        yield runner


@pytest.fixture
def log(caplog):
    caplog.set_level(logging.INFO)
    return caplog