"""Bing Search"""

from datetime import datetime
import json
import os
# import time
import warnings
import requests

TIMEOUT_SEC: float = 30.0
WAIT_TIME_SEC: float = 3.0
MARKET_DEFAULT: str = 'en-US'
DEFAULT_OUTPUT_DIRPATH: str = r'C:\home\local\test\data\bing_search'
DATETIME_FORMAT: str = '%Y%m%d%H%M%S'

KEY_BING: str | None = os.environ.get("AZURE_BING_KEY", None)
ENDPOINT_BING_BASE: str | None = os.environ.get("AZURE_BING_ENDPOINT", None)
ENDPOINT_BING: str | None = f"{ENDPOINT_BING_BASE.rstrip('/')}/v7.0/search"
ENDPOINT_LOCATION: str | None = os.environ.get("AZURE_BING_LOCATION", None)


def save(fpath: str, value: dict):
    """Saves a dictionary to a JSON file.

    This function serializes a Python dictionary into JSON format and writes it to a specified file.

    Args:
        fpath (str): The path to the file where the JSON data will be saved.
        value (dict): The Python dictionary to be serialized and saved.
    """
    with open(fpath, "w", encoding="utf-8") as ff:
        json.dump(value, ff, indent=4)


def search(query: str, mkt: str = MARKET_DEFAULT) -> dict:
    """Searches the web using the Microsoft Bing Search API.

    Args:
        query (str): The search query.
        mkt (str, optional): The market to target for the search. Defaults to MARKET_DEFAULT.

    Returns:
        dict: A JSON dictionary containing the search results, or None if no API key is provided.

    Raises:
        requests.exceptions.RequestException: If there is an error making the request.

    Notes:
        This function requires a valid Azure Bing Search API key to be set.
        The returned JSON dictionary structure is subject to change based on the Bing Search API.
    """
    if not KEY_BING:
        warnings.warn("No key for Azure Bing Search allocated.")
        return None
    headers = {'Ocp-Apim-Subscription-Key': KEY_BING}
    params: dict = {'q': query, 'mkt': mkt}
    response = requests.get(
        ENDPOINT_BING, headers=headers,
        params=params, timeout=TIMEOUT_SEC
    )
    response.raise_for_status()
    return response.json()


def main(query: str, mkt: str = MARKET_DEFAULT, dst: str = ""):
    """main"""
    response = search(query, mkt)
    if not dst:
        now: str = datetime.now().strftime(DATETIME_FORMAT)
        dst = os.path.join(DEFAULT_OUTPUT_DIRPATH, f"{now}_result.json")
    if not os.path.exists(os.path.dirname(dst)):
        os.makedirs(os.path.dirname(dst))
    save(dst, response)


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
