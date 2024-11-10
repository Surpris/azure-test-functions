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

It is desirable to set the following environmental variables before using each function in this module. You can set them by importing the corresponding constants in this module.

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

# Installation

## `pip install` from repository

```sh
pip install git+https://github.com/Surpris/azure-test-functions.git
```

## `git clone` and `pip install`

```sh
git clone https://github.com/Surpris/azure-test-functions.git
cd azure-test-functions
pip install .
```

# Usage

## bing_search

CLI:

```sh
azure_test_bing_search <your_query> \
    --mkt <your_market> \
    --dst <dir_path_to_save_result_in>
```

`python -m`:

```sh
python -m azure_test_functions.bing_search <your_query> \
    --mkt <your_market> \
    --dst <dir_path_to_save_result_in>
```

## gpt

CLI:

```sh
azure_test_gpt <your_query> \
    --dst <destination_dir_path> \
    --max_tokens <max_tokens_of_response>
```

`python -m`:

```sh
python -m azure_test_functions.gpt <your_query> \
    --dst <destination_dir_path> \
    --max_tokens <max_tokens_of_response>
```

## ocr

CLI:

```sh
azure_test_ocr <file_path_or_dir_path>
```

`python -m`:

```sh
python -m azure_test_functions.ocr <file_path_or_dir_path>
```

### merge_texts for ocr

You can use a CLI command `azure_test_merge_texts` to merge texts in the output of `azure_test_ocr`:

```sh
azure_test_ocr_merge_texts <ocr_result_file_path_or_dir_path> \
    --bounding_rect upper_left_x upper_left_y lower_right_x lower_right_y \
    --dst <dst_file_path_or_dir_path>
```

## speech_to_text

CLI:

```sh
azure_test_speech_to_text <file_path_or_dir_path> \
    --dst <dst_file_path_or_dir_path> \
    --la <language_to> --fast_mode
```

`python -m`:

```sh
python -m azure_test_functions.speech_to_text <file_path_or_dir_path> \
    --dst <dst_file_path_or_dir_path> \
    --la <language_to> --fast_mode
```

## translation

CLI:

```sh
azure_test_translation <file_path_or_dir_path> \
    --la <language_to>
```

`python -m`:

```sh
python -m azure_test_functions.translation <file_path_or_dir_path> \
    --la <language_to>
```
