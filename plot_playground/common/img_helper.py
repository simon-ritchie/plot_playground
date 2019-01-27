"""
A module that provides image helper functions.
"""

import os

import cv2


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


def compare_img_hist(img_path_1, img_path_2, img_width, img_height):
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
    img_width : int
        Image width.
    img_height : int
        Image height.

    Returns
    -------
    similarity : float
        Similarity between two images. The maximum is set to 1.0, and the
        closer to 1.0, the higher the similarity.
    """
    pass
