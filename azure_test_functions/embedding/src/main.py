"""embedding"""

import os
# from openai import AzureOpenAI

TIMEOUT_SEC: float = 30.0
WAIT_TIME_SEC: float = 3.0
DSTDIR_DEFAULT: str = r'C:\home\local\test\data\embedding'
DATETIME_FORMAT: str = '%Y%m%d%H%M%S'

ENDPOINT_KEY: str | None = os.environ.get("AZURE_OPENAI_KEY", None)
ENDPOINT_BASE: str | None = os.environ.get("AZURE_OPENAI_ENDPOINT", None)
MODEL: str | None = os.environ.get("AZURE_OPENAI_EMBEDDING_MODEL", None)
API_VERSION: str | None = os.environ.get("AZURE_OPENAI_EMBEDDING_API_VERSION", None)
EMBEDDING_ENDPOINT: str | None = None
if ENDPOINT_BASE is not None:
    EMBEDDING_ENDPOINT = f"{ENDPOINT_BASE.rstrip('/')}/openai/deployments/{MODEL}/embeddings?api-version={API_VERSION}"
LOCATION: str | None = os.environ.get("AZURE_OPENAI_EMBEDDING_LOCATION", None)
