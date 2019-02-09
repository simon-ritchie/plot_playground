"""
Module describing general purpose processing of
Selenium's webdriver control.
"""

import time
import subprocess as sp
import os
from io import BytesIO

import chromedriver_binary
from selenium import webdriver
import logging
from PIL import Image
from selenium.webdriver.common.keys import Keys

from plot_playground.common import settings

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
    time.sleep(3)


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


DEFAULT_TEST_IMG_PATH = os.path.join(
    settings.ROOT_DIR,
    'plot_playground',
    'tests',
    'tmp_test_img.png'
)


def save_target_elem_screenshot(
        target_elem, img_path=DEFAULT_TEST_IMG_PATH):
    """
    Save screenshot of target element.

    Parameters
    ----------
    target_elem : selenium.webdriver.remote.webelement.WebElement
        The WebElement for which screen shots are to be taken.
    img_path : str, default DEFAULT_TEST_IMG_PATH
        The destination path.
    """

    driver.find_element_by_tag_name('body').send_keys(
        Keys.CONTROL + Keys.HOME)
    location_dict = target_elem.location
    size_dict = target_elem.size
    elem_x = location_dict['x']
    left = location_dict['x']
    top = location_dict['y']
    right = location_dict['x'] + size_dict['width']
    bottom = location_dict['y'] + size_dict['height']
    screenshot_png = driver.get_screenshot_as_png()
    with Image.open(BytesIO(screenshot_png)) as img:
        img = img.crop((left, top, right, bottom))
        img.save(img_path)
