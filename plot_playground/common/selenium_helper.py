"""
Module describing general purpose processing of
Selenium's webdriver control.
"""

import chromedriver_binary
from selenium import webdriver

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
