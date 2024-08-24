"""bing_search"""

from .src.main import main, MARKET_DEFAULT

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("query", type=str)
    parser.add_argument(
        "--mkt", dest="mkt", type=str, default=MARKET_DEFAULT
    )
    parser.add_argument(
        "--dst", dest="dst", type=str, default=""
    )
    args = parser.parse_args()
    main(args.query, args.mkt, args.dst)
