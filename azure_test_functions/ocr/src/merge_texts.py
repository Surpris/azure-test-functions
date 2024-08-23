"""merge_texts.py"""

import json
import os

DEFAULT_OUTPUT_DIRNAME: str = "merged"

def extract_texts(src: dict) -> str:
    texts = " ".join(
        line["text"] for line in src["readResult"]["blocks"][0]["lines"]
    )
    return texts


def main(dirpath: str):
    """Processes JSON files in a directory and extracts text.

    This function iterates over JSON files in the specified directory, extracts text
    content from each file, and saves the extracted text to corresponding .txt files
    in a designated output directory.

    Args:
        dirpath (str): The path to the directory containing JSON files.

    Raises:
        NotADirectoryError: If the provided `dirpath` is not a directory.
    """
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
        texts: str = extract_texts(data)
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
    args = parser.parse_args()
    main(args.src)
