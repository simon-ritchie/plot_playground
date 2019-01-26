"""
A module that define constans, settings, etc.
"""

import sys
import os

ROOT_DIR = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        os.pardir,
        os.pardir))

D3_VERSION = '4'

JUPYTER_TEST_PORT = 18080

TEST_SVG_ELEM_ID = 'test_svg'
