"""
Test Command
------------
$ python run_tests.py --module_name plot_playground.tests.test_vaxis
"""

from nose.tools import assert_equal, assert_true

from plot_playground.axis import vaxis


def test__get_y_baseline():
    """
    Test Command
    ------------
    $ python run_tests.py --module_name plot_playground.tests.test_vaxis:test__get_y_baseline --skip_jupyter 1
    """
    y_baseline = vaxis._get_y_baseline(data_list=[1, 2])
    assert_equal(y_baseline, 0)

    y_baseline = vaxis._get_y_baseline(data_list=[-1, 3])
    assert_equal(y_baseline, -1)
