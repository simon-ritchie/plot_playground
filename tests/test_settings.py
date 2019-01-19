import os

from nose.tools import assert_equal, assert_true
from plot_playground.common import settings


def test_ROOT_DIR():
    assert_true(
        settings.ROOT_DIR.endswith('plot_playground'))


def test_D3_PATH():
    assert_true(
        os.path.exists(settings.D3_PATH))
