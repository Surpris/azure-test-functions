"""ocr"""

from .src.main import main, LANGUAGE, SUPPORTED_LANGUAGES

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
    parser.add_argument(
        "--fast_mode", dest="fast_mode", action="store_true"
    )
    parser.add_argument(
        "--list-lang", dest="list_lang", action="store_true",
        help="list the supported languages"
    )
    args = parser.parse_args()
    if args.la not in SUPPORTED_LANGUAGES:
        raise ValueError(
            f"language '{args.la}' is not supported. "
            f"supported languages are {SUPPORTED_LANGUAGES}."
        )
    if args.list_lang:
        print("supported languages:", SUPPORTED_LANGUAGES)
        exit(0)
    if args.fast_mode:
        print("use the fast transcription API.")
    main(args.src, args.la, args.fast_mode)
