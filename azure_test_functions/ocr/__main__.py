"""ocr"""

from .src.main import main

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("src", type=str)
    args = parser.parse_args()
    main(args.src)
