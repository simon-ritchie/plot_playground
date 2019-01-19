# coding: UTF-8

import os
from setuptools import setup, find_packages

readme_str = """Please see github document for detail information.
"""

setup(
    name='plot_playground',
    version='0.0.1',
    url='https://github.com/simon-ritchie/plot_playground',
    author='simon-ritchie',
    author_email='antisocial.sid2@gmail.com',
    maintainer='simon-ritchie',
    maintainer_email='antisocial.sid2@gmail.com',
    description='plot playground is a plot library that works on Jupyter and Pandas datasets.',
    long_description=readme_str,
    packages=find_packages(),
    install_requires=[],
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'License :: OSI Approved :: MIT License',
    ],
),
