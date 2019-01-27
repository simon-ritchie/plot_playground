"""
A module that provides image helper functions.
"""

import os

import numpy as np
import cv2

from plot_playground.common import settings


def assert_img_exists(img_path):
    """
    Check that the image exists in the specified path.

    Parameters
    ----------
    img_path : str
        Path of image to be checked.

    Raises
    ------
    AssertionError
        If there is no image in the specified path.
    """
    if os.path.exists(img_path):
        return
    err_msg = 'There is no image in the specified path: %s' % img_path
    raise AssertionError(err_msg)


def compare_img_hist(img_path_1, img_path_2):
    """
    Get the comparison result of the similarity by the histogram of the
    two images. This is suitable for checking whether the image is close
    in color. Conversely, it is not suitable for checking whether shapes
    are similar.

    Parameters
    ----------
    img_path_1 : str
        The path of the first image for comparison.
    img_path_2 : str
        The path of the second image for comparison.

    Returns
    -------
    similarity : float
        Similarity between two images. The maximum is set to 1.0, and the
        closer to 1.0, the higher the similarity. It is set by the mean
        value of the histogram of RGB channels.
    """
    assert_img_exists(img_path=img_path_1)
    assert_img_exists(img_path=img_path_2)
    img_1 = cv2.imread(img_path_1)
    img_2 = cv2.imread(img_path_2)
    channels_list = [[0], [1], [2]]
    similarity_list = []

    for channels in channels_list:
        img_1_hist = cv2.calcHist(
            images=[img_1],
            channels=channels,
            mask=None,
            histSize=[256],
            ranges=[0, 256]
        )
        img_2_hist = cv2.calcHist(
            images=[img_2],
            channels=channels,
            mask=None,
            histSize=[256],
            ranges=[0, 256]
        )
        similarity_unit = cv2.compareHist(
            H1=img_1_hist, H2=img_2_hist, method=cv2.HISTCMP_CORREL)
        similarity_list.append(similarity_unit)
    similarity = np.mean(similarity_list)
    return similarity


def get_test_expected_img_path(file_name):
    """
    Get the path of the assumed image for the test.

    Parameters
    ----------
    file_name : str
        The file name of the target excluding the extension.

    Returns
    -------
    img_path : str
        Path of target image.
    """
    img_path = os.path.join(
        settings.ROOT_DIR,
        'plot_playground',
        'tests',
        'expected_img',
        '%s.png' % file_name,
    )
    return img_path
