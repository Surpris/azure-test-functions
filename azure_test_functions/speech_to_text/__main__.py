"""ocr"""

from .src.main import main, LANGUAGE

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("src", type=str, help="the path of dir or audio file")
    parser.add_argument(
        "--la", dest="la", default=LANGUAGE,
        help="language to transcribe the file(s) in"
    )
    parser.add_argument(
        "--same_level", dest="same_level", action="store_true"
    )
    args = parser.parse_args()
    main(args.src, args.la)
