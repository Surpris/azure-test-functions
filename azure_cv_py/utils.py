"""
Utility functions.
"""

import os


def set_key(key: str) -> None:
    """
    set your key for the Azure Computer Vision.

    Paramtetrs
    ==========
    key: str
        your key.
    """
    os.environ['COMPUTER_VISION_KEY'] = key


def set_endpoint(endpoint: str) -> None:
    """
    set your endpoint of the Azure Computer Vision.

    Paramtetrs
    ==========
    endpoint: str
        your endpoint.
    """
    os.environ['COMPUTER_VISION_ENDPOINT'] = endpoint
