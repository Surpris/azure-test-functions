"""gpt

GPT test
"""

from datetime import datetime
import os
import warnings
from openai import AzureOpenAI
from openai.types.chat import ChatCompletionMessageParam, ChatCompletion

MAX_TOKENS: int = 50
TIMEOUT_SEC: float = 30.0
WAIT_TIME_SEC: float = 3.0
DEFAULT_OUTPUT_DIRPATH: str = r'C:\home\local\test\data\gpt'
DATETIME_FORMAT: str = '%Y%m%d%H%M%S'

ENDPOINT_KEY: str | None = os.getenv("AZURE_OPENAI_KEY")
ENDPOINT_BASE: str = os.environ.get("AZURE_OPENAI_ENDPOINT", "")
MODEL: str = os.environ.get("AZURE_OPENAI_CHAT_MODEL", "")
API_VERSION: str | None = os.getenv("AZURE_OPENAI_CHAT_API_VERSION")
# LOCATION: str | None = os.getenv("AZURE_OPENAI_LOCATION")

CLIENT = AzureOpenAI(
    api_key=ENDPOINT_KEY,
    api_version=API_VERSION,
    azure_endpoint=ENDPOINT_BASE
)


def save(fpath: str, value: str) -> None:
    """Saves a string to a specified file.

    Args:
        fpath (str): The path to the file where the string will be saved.
        value (str): The string to be saved.

    Raises:
        IOError: If there is an error writing to the file.

    """
    with open(fpath, "w", encoding="utf-8") as ff:
        ff.write(value)


def chat(query: str, max_tokens: int = MAX_TOKENS) -> str | None:
    """Sends a message to the Azure OpenAI Chat Completions API
    and returns the generated response.

    Args:
        query (str): The text message to send to the model.
        max_tokens (int, optional): The maximum number of tokens to generate
                                    in the response. Defaults to MAX_TOKENS.

    Returns:
        str: The generated text response.

    Raises:
        Exception: If there is an error communicating with the Azure OpenAI service.

    This function utilizes the Azure OpenAI Chat Completions API
    to generate text completions based on the provided prompt.
    It constructs a message object with the role 'user' and the given content,
    and then sends it to the API.
    The `max_tokens` parameter controls the length of the generated response.
    """
    message: ChatCompletionMessageParam = {'role': 'user', 'content': query}
    response: ChatCompletion = CLIENT.chat.completions.create(
        messages=[message], model=MODEL, max_tokens=max_tokens
    )
    return response.choices[0].message.content


def main(message: str, dst: str = "", max_tokens: int = MAX_TOKENS) -> None:
    """main"""
    print("chat test starts.")
    content = chat(message, max_tokens)
    if content is None:
        warnings.warn("No content returned. finish.")
        return
    if not dst:
        now: str = datetime.now().strftime(DATETIME_FORMAT)
        dst = os.path.join(DEFAULT_OUTPUT_DIRPATH, f"{now}_result.txt")
    if not os.path.exists(os.path.dirname(dst)):
        os.makedirs(os.path.dirname(dst))
    save(dst, content)
    print("finished.")


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
