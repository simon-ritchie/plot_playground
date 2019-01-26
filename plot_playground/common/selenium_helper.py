"""
Module describing general purpose processing of
Selenium's webdriver control.
"""

import subprocess as sp
import os

import chromedriver_binary
from selenium import webdriver
import logging

selenium_logger = logging.getLogger(
    'selenium.webdriver.remote.remote_connection')
selenium_logger.setLevel(logging.WARNING)

driver = None


def start_webdriver():
    """
    Start the Selenium webdriver process.

    Returns
    -------
    driver : selenium.webdriver.Chrome
        Target webdriver.

    Notes
    -----
    If webdriver has already been started, it is
    stopped beforehand.
    """
    global driver
    if driver is not None:
        exit_webdriver()
    driver = webdriver.Chrome()
    return driver


def exit_webdriver():
    """
    Stop the running webdriver.
    """
    global driver
    if driver is None:
        return
    driver.close()
    driver = None


def chromedriver_process_exists():
    """
    Get a boolean on whether Chromedriver's process exists.

    Returns
    -------
    result : bool
        True is set if it exists.
    """
    out = sp.check_output(
        'tasklist /fi "imagename eq chromedriver.exe"',
        shell=True)
    out = str(out)
    is_in = 'chromedriver.exe' in out
    if not is_in:
        return False
    return True


def kill_chromedriver_process():
    """
    If the process of running chromedriver remains, stop
    that process.
    """
    if not chromedriver_process_exists():
        return
    os.system('taskkill /im chromedriver.exe /f')
