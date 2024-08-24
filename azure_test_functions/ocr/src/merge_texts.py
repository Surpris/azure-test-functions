"""merge_texts.py"""

import json
import os

DEFAULT_OUTPUT_DIRNAME: str = "merged"


def is_in_bounding_rect(src: list, bounding: list) -> bool:
    if src[0] < bounding[0]:
        return False
    if src[1] < bounding[1]:
        return False
    if src[2] > bounding[2]:
        return False
    if src[3] > bounding[3]:
        return False
    return True


def extract_texts(src: dict, bounding_rect: list | None = None) -> str:
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
        texts_in = [line for line in src["readResult"]["blocks"][0]["lines"]]
    return " ".join(texts_in)


def main(dirpath: str, bounding_rect: list | None = None):
    """Processes JSON files in a directory and extracts text.

    This function iterates over JSON files in the specified directory, extracts text
    content from each file, and saves the extracted text to corresponding .txt files
    in a designated output directory.

    Args:
        dirpath (str): The path to the directory containing JSON files.

    Raises:
        NotADirectoryError: If the provided `dirpath` is not a directory.
    """
    print("obu", bounding_rect)
    if not os.path.isdir(dirpath):
        raise NotADirectoryError("'src' must be a directory path.")
    dstdir: str = os.path.join(dirpath, DEFAULT_OUTPUT_DIRNAME)
    if not os.path.exists(dstdir):
        os.makedirs(dstdir)

    for fname in sorted(os.listdir(dirpath)):
        fpath = os.path.join(dirpath, fname)
        if not os.path.isfile(fpath):
            continue
        data = None
        with open(fpath, "r", encoding="utf-8") as ff:
            data = json.load(ff)
        texts: str = extract_texts(data, bounding_rect)
        dstpath_target = os.path.join(
            dstdir,
            os.path.basename(fname).replace(
                os.path.splitext(fname)[-1],
                ".txt"
            )
        )
        with open(dstpath_target, "w", encoding="utf-8") as ff:
            ff.write(texts)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("src", type=str)
    parser.add_argument(
        "--bounding_rect", dest="bounding_rect", nargs=4,
        type=int, default=None
    )
    args = parser.parse_args()
    main(args.src, args.bounding_rect)
