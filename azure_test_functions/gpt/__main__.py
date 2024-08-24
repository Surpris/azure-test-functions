"""gpt"""

from .src.main import main, MAX_TOKENS

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("query", type=str)
    parser.add_argument(
        "--dst", dest="dst", type=str, default=""
    )
    parser.add_argument(
        "--max_tokens", dest="max_tokens", type=str, default=MAX_TOKENS
    )
    args = parser.parse_args()
    main(args.query, args.dst, args.max_tokens)
