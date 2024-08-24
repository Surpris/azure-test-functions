"""translation"""

from .src.main import main, LANGUAGE_TO

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("src", type=str)
    parser.add_argument(
        "--la", dest="la", type=str, default=LANGUAGE_TO
    )
    args = parser.parse_args()
    main(args.src, args.la)
