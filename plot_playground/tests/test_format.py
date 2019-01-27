"""
Test Command
------------
$ python run_tests.py --module_name plot_playground.tests.test_format --skip_jupyter 1
"""

from copy import deepcopy

from nose.tools import assert_equal, assert_true

from plot_playground.common import format


def test_convert_list_value_by_format():
    """
    Test Command
    ------------
    $ python run_tests.py --module_name plot_playground.tests.test_format:test_convert_list_value_by_format --skip_jupyter 1
    """

    data_list = [1.3333, 2.6666, 3.2222]

    result_list = format.convert_list_value_by_format(
        data_list=deepcopy(data_list),
        format=format.FORMAT.INT)
    assert_equal(result_list, [1, 2, 3])

    result_list = format.convert_list_value_by_format(
        data_list=deepcopy(data_list),
        format=format.FORMAT.FLOAT_1)
    assert_equal(result_list, [1.3, 2.7, 3.2])

    result_list = format.convert_list_value_by_format(
        data_list=deepcopy(data_list),
        format=format.FORMAT.FLOAT_2)
    assert_equal(result_list, [1.33, 2.67, 3.22])

    result_list = format.convert_list_value_by_format(
        data_list=deepcopy(data_list),
        format=format.FORMAT.FLOAT_3)
    assert_equal(result_list, [1.333, 2.667, 3.222])
