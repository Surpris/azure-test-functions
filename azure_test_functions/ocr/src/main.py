"""ocr"""

import json
import os
import time
from typing import Dict, Any
from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
from azure.core.credentials import AzureKeyCredential

TIMEOUT_SEC: float = 30.0
WAIT_TIME_SEC: float = 3.0
DEFAULT_OUTPUT_DIRNAME: str = "analyzed"

KEY_CV: str = os.environ.get("AZURE_CV_KEY", "")
ENDPOINT_BASE: str = os.environ.get("AZURE_CV_ENDPOINT", "")

# Create an Image Analysis client
CLIENT = ImageAnalysisClient(
    endpoint=ENDPOINT_BASE,
    credential=AzureKeyCredential(KEY_CV),
    timeout=TIMEOUT_SEC
)


def save(fpath: str, value: Dict[str, Any]) -> None:
    """Saves a dictionary to a JSON file.

    This function serializes a Python dictionary into JSON format and writes it to a specified file.

    Args:
        fpath (str): The path to the file where the JSON data will be saved.
        value (dict): The Python dictionary to be serialized and saved.
    """
    with open(fpath, "w", encoding="utf-8") as ff:
        json.dump(value, ff, indent=4)


def analyze(fpath: str) -> Dict[str, Any]:
    """Analyzes an image using the Azure Computer Vision.

    This function takes the path to an image file, reads the image data, 
    and sends it to the Azure Computer Vision for analysis.
    The function returns the analysis results as a dictionary.

    Args:
        fpath (str): The path to the image file to be analyzed.

    Returns:
        dict: A dictionary containing the analysis results. The specific structure of the 
              dictionary will depend on the image analysis service being used.
    """
    image_data: bytes = bytes()
    with open(fpath, "rb") as ff:
        image_data = ff.read()

    result = CLIENT.analyze(
        image_data,
        visual_features=[VisualFeatures.READ]
    )
    return result.as_dict()


def analyze_from_dir(src: str) -> None:
    """Analyzes images in a directory and saves results as JSON files.

    This function iterates over image files in the specified directory, analyzes each image
    using the `analyze` function, and saves the analysis results as JSON files in a designated
    output directory.

    Args:
        src (str): The path to the directory containing image files.

    Raises:
        ValueError: If the provided `src` is not a directory.
    """
    if not os.path.isdir(src):
        raise ValueError("'src' must be a directory path.")
    dstdir: str = os.path.join(src, DEFAULT_OUTPUT_DIRNAME)
    if not os.path.exists(dstdir):
        os.makedirs(dstdir)

    # analyzed_list = []
    filename_list = [
        fname for fname in os.listdir(src)
        if os.path.isfile(os.path.join(src, fname))
    ]
    n_files = len(filename_list)
    print(f"# of files: {n_files}")
    for ii, fname in enumerate(filename_list):
        print(f"target: {fname} ({ii + 1}/{n_files})")
        if not os.path.isfile(os.path.join(src, fname)):
            continue
        dstpath_target = os.path.join(
            dstdir,
            os.path.basename(fname).replace(
                os.path.splitext(fname)[-1],
                ".json"
            )
        )
        if os.path.exists(dstpath_target):
            print("already analyzed. skip")
            # with open(dstpath_target, "r", encoding="utf-8") as ff:
            #     analyzed = json.load(ff)
            # analyzed_list.append(analyzed)
            continue
        analyzed = analyze(os.path.join(src, fname))
        # if analyzed is None:
        #     print("failure in analysis. skip.")
        #     time.sleep(WAIT_TIME_SEC)
        #     continue
        # analyzed_list.append(analyzed)
        save(dstpath_target, analyzed)
        print("done.")
        time.sleep(WAIT_TIME_SEC)


def main(fpath: str) -> None:
    """Analyzes an image or a directory of images.

    This function determines whether the provided path is a file or a directory.
    If it's a file, it analyzes the image and saves the results as a JSON file.
    If it's a directory, it recursively analyzes all images within the directory and saves
    the results as JSON files in a subdirectory.

    Args:
        fpath (str): The path to an image file or a directory containing images.

    Raises:
        ValueError: If the analysis fails or if the provided path is invalid.
    """
    if os.path.isdir(fpath):
        analyze_from_dir(fpath)
    else:
        translated = analyze(fpath)
        if translated is None:
            raise ValueError("failure in analysis.")
        dstdir = os.path.join(
            os.path.dirname(fpath), DEFAULT_OUTPUT_DIRNAME
        )
        if not os.path.exists(dstdir):
            os.makedirs(dstdir)
        dstpath_target = os.path.join(
            dstdir,
            os.path.basename(fpath).replace(
                os.path.splitext(fpath)[-1],
                ".json"
            )
        )
        save(dstpath_target, translated)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("src", type=str)
    args = parser.parse_args()
    main(args.src)
