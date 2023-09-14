"""
Functions using the OCR API.
"""

import os
import requests
from .constants import OCR_API_ENDPOINT


def extract_characters_with_azure_cv_ocr(image_path: str) -> dict:
    """
    extract characters in an image by using the Azoure CV OCR API.

    Parameters
    ==========
    image_path : str
        path of an image.

    Returns
    =======
    dict : the result of OCR.
    """
    # Validate the key and the endpoint.
    if os.environ.get('COMPUTER_VISION_KEY', None) is None:
        raise Exception(
          'No key found. please set your key for the Azure Computer Vision to the env path "COMPUTER_VISION_KEY."'
        )
    if os.environ.get('COMPUTER_VISION_ENDPOINT', None) is None:
        raise Exception(
            'No endpoint found. please set your endpoint of the Azure Computer Vision to the env path "COMPUTER_VISION_ENDPOINT."'
        )

    # Read the image into a byte array
    image_data = open(image_path, "rb").read()

    # Set Content-Type to octet-stream
    headers = {
        'Ocp-Apim-Subscription-Key': os.environ['COMPUTER_VISION_KEY'],
        'Content-Type': 'application/octet-stream'
    }

    # Set parameters
    params = {'language': 'unk', 'detectOrientation': 'true'}

    # put the byte array into your post request
    ocr_url = f"{os.environ['COMPUTER_VISION_ENDPOINT'].rstrip('/')}/{OCR_API_ENDPOINT}"
    response = requests.post(ocr_url, headers=headers, params=params, data=image_data)
    response.raise_for_status()

    return response.json()


def extract_full_text(response: dict) -> str:
    """
    extract the full text from a resonse dict.

    Paramters
    =========
    response : dict
        a response from the Azure CV OCR API.

    Returns
    =======
    str : a full text in the resopnse.
    """
    line_infos = [region["lines"] for region in response["regions"]]
    text_infos = []
    for line in line_infos:
        for word_metadata in line:
            for word_info in word_metadata["words"]:
                text_infos.append(word_info["text"])
    return " ".join(text_infos)


def extract_and_save_full_text_with_azure_cv_ocr(image_path: str, dst_path: str) -> None:
    """
    extract ande save the full text in an image by using the Azure CV OCR API.

    Parameters
    ==========
    image_path : str
        path of an image.
    dst_path : str
        path of the destination file.
    """
    response = extract_characters_with_azure_cv_ocr(image_path)
    text = extract_full_text(response)
    with open(dst_path, "w") as ff:
        ff.write(text)
