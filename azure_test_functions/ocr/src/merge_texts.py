"""merge_texts.py"""

import json
import os

DEFAULT_OUTPUT_DIRNAME: str = "merged"


def is_in_bounding_rect(src: list, bounding: list) -> bool:
    """Checks if a source rectangle is completely contained within a bounding rectangle.

    Args:
        src (list): A list representing the source rectangle in the format [x1, y1, x2, y2].
        bounding (list): A list representing the bounding rectangle in the same format.

    Returns:
        bool: True if the source rectangle is completely contained
              within the bounding rectangle, False otherwise.

    Raises:
        ValueError: If either `src` or `bounding` is not a list of length 4.

    Examples:
        >>> is_in_bounding_rect([10, 10, 20, 20], [0, 0, 30, 30])
        True
        >>> is_in_bounding_rect([30, 30, 40, 40], [0, 0, 30, 30])
        False
    """
    if src[0] < bounding[0]:
        return False
    if src[1] < bounding[1]:
        return False
    if src[2] > bounding[2]:
        return False
    if src[3] > bounding[3]:
        return False
    return True


def save(fpath: str, value: str):
    """Saves a string to a specified file.

    Args:
        fpath (str): The path to the file where the string will be saved.
        value (str): The string to be saved.

    Raises:
        IOError: If there is an error writing to the file.

    """
    with open(fpath, "w", encoding="utf-8") as ff:
        ff.write(value)


def extract_texts(src: dict, bounding_rect: list | None = None) -> str:
    """Extracts text from a given source within an optional bounding rectangle.

    Args:
        src (dict): A dictionary containing OCR results, typically in a format
            returned by the Azure Computer Vision for analysis API.
        bounding_rect (list, optional): A list representing the bounding rectangle
            in the format [x1, y1, x2, y2].
            If provided, only text within this rectangle is extracted.
            Defaults to None, which extracts all text.

    Returns:
        str: A string containing the extracted text.

    Raises:
        KeyError: If the `src` dictionary does not have the expected structure.
    """
    texts_in: list = []
    if bounding_rect is not None:
        for line in src["readResult"]["blocks"][0]["lines"]:
            bounding_ = [
                line["boundingPolygon"][0]["x"],
                line["boundingPolygon"][0]["y"],
                line["boundingPolygon"][2]["x"],
                line["boundingPolygon"][2]["y"],
            ]
            if is_in_bounding_rect(bounding_, bounding_rect):
                texts_in.append(line["text"])
    else:
        texts_in = src["readResult"]["blocks"][0]["lines"]
    return " ".join(texts_in)


def extract_texts_from_file(
    src: str, bounding_rect: list | None = None,
    dst: str | None = None
) -> str | None:
    """Extracts text from a JSON file containing OCR results,
    optionally within a specified bounding rectangle,
    and saves the extracted text to a given path.

    Args:
        src (str): The path to the JSON file containing OCR results.
        bounding_rect (list, optional): A list representing the bounding rectangle
            in the format [x1, y1, x2, y2].
            If provided, only text within this rectangle is extracted.
            Defaults to None, which extracts all text.
        dst (str, optional): A file path to save the extracted text in.

    Returns:
        str or None: A string containing the extracted text,
        or None if the file cannot be read or the JSON data is invalid.

    Raises:
        FileNotFoundError: If the specified file cannot be found.
        json.JSONDecodeError: If the JSON data in the file is invalid.
    """
    data: dict | None = None
    with open(src, "r", encoding="utf-8") as ff:
        data = json.load(ff)
    texts: str = extract_texts(data, bounding_rect)
    if dst is not None:
        save(dst, texts)
    return texts


def extract_texts_from_dir(
    src: str, bounding_rect: list | None = None,
    dst_dir_path: str | None = None
) -> list:
    """Extracts text from all JSON files in a given directory
    and saves the extracted text to a given directory.

    Args:
        src (str): The path to the directory containing JSON files with OCR results.
        bounding_rect (list, optional): A list representing the bounding rectangle
            in the format [x1, y1, x2, y2].
            If provided, only text within this rectangle is extracted.
            Defaults to None, which extracts all text.
        dst_dir_path (str, optional): A directory path to save the extracted texts in.

    Returns:
        list of str or None: A list containing the extracted texts or None.

    Raises:
        NotADirectoryError: If the specified path is not a directory.
        FileNotFoundError: If a JSON file cannot be found or read.
        json.JSONDecodeError: If the JSON data in a file is invalid.
    """
    if not os.path.isdir(src):
        raise NotADirectoryError("'src' must be a directory path.")
    if dst_dir_path is not None and not os.path.isdir(dst_dir_path):
        raise NotADirectoryError("'dst_dir_path' must be a directory path.")

    dst: list = []
    for fname in sorted(os.listdir(src)):
        fpath = os.path.join(src, fname)
        if not os.path.isfile(fpath):
            continue
        dst_fpath: str | None = None
        if dst_dir_path is not None:
            dst_fpath = os.path.join(
                dst_dir_path,
                os.path.basename(fname).replace(
                    os.path.splitext(fname)[-1],
                    ".txt"
                )
            )
        dst.append(extract_texts_from_file(
            fpath, bounding_rect, dst_fpath
        ))

    return dst


def main(
    file_or_dir_path: str, bounding_rect: list | None = None,
    dst_file_or_dir_path: str | None = None
):
    """Extracts text from a given file or directory and saves the results to a specified destination.

    Args:
        file_or_dir_path (str): The path to the file or directory containing OCR results.
        bounding_rect (list, optional): A list representing the bounding rectangle
            in the format [x1, y1, x2, y2].
            If provided, only text within this rectangle is extracted.
            Defaults to None, which extracts all text.
        dst_file_or_dir_path (str, optional): The path to the destination file
            or directory where the extracted text will be saved.
            If not provided, a default output directory will be created
            within the source directory.

    Raises:
        ValueError: If `file_or_dir_path` is not a valid file or directory path.
        NotADirectoryError: If `file_or_dir_path` is a directory
            but `dst_file_or_dir_path` is not provided.
    """
    print("extract...")
    if os.path.isdir(file_or_dir_path):
        if dst_file_or_dir_path is None:
            dst_file_or_dir_path = os.path.join(
                file_or_dir_path, DEFAULT_OUTPUT_DIRNAME
            )
        if not os.path.exists(dst_file_or_dir_path):
            os.makedirs(dst_file_or_dir_path)
        _ = extract_texts_from_dir(
            file_or_dir_path, bounding_rect,
            dst_file_or_dir_path
        )
    elif os.path.isfile(file_or_dir_path):
        if dst_file_or_dir_path is None:
            dst_dir_path: str = os.path.join(
                os.path.dirname(file_or_dir_path), DEFAULT_OUTPUT_DIRNAME
            )
            if not os.path.exists(dst_dir_path):
                os.makedirs(dst_dir_path)
            dst_file_or_dir_path = os.path.join(
                dst_dir_path,
                os.path.basename(file_or_dir_path).replace(
                    os.path.splitext(file_or_dir_path)[-1],
                    ".txt"
                )
            )
        _ = extract_texts_from_file(
            file_or_dir_path, bounding_rect, dst_file_or_dir_path
        )
    else:
        raise ValueError(
            "`file_or_dir_path` must be a file od directory path."
        )
    print("done.")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("src", type=str)
    parser.add_argument(
        "--bounding_rect", dest="bounding_rect", nargs=4,
        type=int, default=None
    )
    parser.add_argument(
        "--dst", dest="dst",
        type=str, default=None
    )
    args = parser.parse_args()
    main(args.src, args.bounding_rect, args.dst)
