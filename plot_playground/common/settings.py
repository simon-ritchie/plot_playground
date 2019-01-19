"""
A module that define constans, settings, etc.
"""

import sys
import os

ROOT_DIR = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        os.pardir))

D3_PATH = os.path.join(
    ROOT_DIR, 'd3', '4.13.0', 'd3.min.js')
