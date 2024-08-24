"""ocr"""

from .src.main import main

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("src", type=str)
    parser.add_argument(
        "--same_level", dest="same_level", action="store_true"
    )
    args = parser.parse_args()
    main(args.src)
