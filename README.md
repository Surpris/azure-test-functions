# azure-test-functions

Functions using the Microsoft Azure Service.

# Functions

| Function       | Overview                                                  |
| :------------- | :-------------------------------------------------------- |
| bing_search    | search using the Bing Search v7.                          |
| gpt            | chat with a LLM model using the Azure OpenAI Service.     |
| ocr            | recognize texts using the Azure Computer Vision.          |
| speech_to_text | transcribe audio using the Azure AI Service.              |
| translation    | translate texts using the Azure Text Translation Service. |

# Required environmental variables

The following environmental variables have to be set before using this module.

## bing_search

| Key                 | Description               |
| :------------------ | :------------------------ |
| AZURE_BING_KEY      | Key.                      |
| AZURE_BING_ENDPOINT | Endpoint.                 |
| AZURE_BING_LOCATION | Location of the endpoint. |

## gpt

| Key                           | Description  |
| :---------------------------- | :----------- |
| AZURE_OPENAI_KEY              | Key.         |
| AZURE_OPENAI_ENDPOINT         | Endpoint.    |
| AZURE_OPENAI_CHAT_MODEL       | LLM model.   |
| AZURE_OPENAI_CHAT_API_VERSION | API version. |

## ocr

| Key               | Description |
| :---------------- | :---------- |
| AZURE_CV_KEY      | Key.        |
| AZURE_CV_ENDPOINT | Endpoint.   |


## speech_to_text

| Key                          | Description             |
| :--------------------------- | :---------------------- |
| AZURE_SPEECH_KEY             | Key.                    |
| AZURE_SPEECH_ENDPOINT        | Endpoint.               |
| AZURE_SPEECH_ENDPOINT_REGION | Region of the endpoint. |

## translation

| Key                               | Description             |
| :-------------------------------- | :---------------------- |
| AZURE_TRANSLATION_KEY             | Key.                    |
| AZURE_TRANSLATION_ENDPOINT        | Endpoint.               |
| AZURE_TRANSLATION_ENDPOINT_REGION | Region of the endpoint. |

# Usage

## bing_search

```sh
python -m azure-test-functions.bing_search.main <your_query> \
    --mkt <your_market> \
    --dst <destination_dir_path>
```

## gpt

```sh
python -m azure-test-functions.gpt.main <your_query> \
    --dst <destination_dir_path> \
    --max_tokens <max_tokens>
```

## ocr

```sh
python -m azure-test-functions.ocr.main <image_path_or_dir_path>
```

## speech_to_text

```sh
python -m azure-test-functions.speech_to_text.main <image_path_or_dir_path> \
    --dst <destination_dir_path> \
    --max_tokens <max_tokens>
```

## translation

```sh
python -m azure-test-functions.translation.main <image_path_or_dir_path> \
    --la <language_to>
```
