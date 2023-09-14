"""
Utility functions.
"""

import os
from getpass import getpass


def set_key() -> None:
    """
    set your key for the Azure Computer Vision.
    This function is supposed to be used in an interaction mode.
    """
    print("set your key for the Azure Computer Vision:")
    os.environ['COMPUTER_VISION_KEY'] = getpass()


def set_endpoint() -> None:
    """
    set your endpoint of the Azure Computer Vision.
    This function is supposed to be used in an interaction mode.
    """
    print("set your endpoint of the Azure Computer Vision:")
    os.environ['COMPUTER_VISION_ENDPOINT'] = getpass()
