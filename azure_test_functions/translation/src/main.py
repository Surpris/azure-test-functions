"""translation"""

import os
import time
from azure.ai.translation.text import TextTranslationClient
from azure.core.credentials import AzureKeyCredential

TIMEOUT_SEC: float = 30.0
WAIT_TIME_SEC: float = 5.0
DEFAULT_OUTPUT_DIRNAME: str = "translated"
LANGUAGE_FROM: str = "en"
LANGUAGE_TO: str = "ja"
EXCLUDE_SUFFIX: str = "merged"

KEY_TRANSLATION: str = os.environ.get("AZURE_TRANSLATION_KEY", "")
ENDPOINT_BASE: str | None = os.environ.get("AZURE_TRANSLATION_ENDPOINT", None)
ENDPOINT_REGION: str | None = os.environ.get("AZURE_TRANSLATION_ENDPOINT_REGION", None)

# Create an Image Analysis client
CLIENT = TextTranslationClient(
    endpoint=ENDPOINT_BASE,
    credential=AzureKeyCredential(KEY_TRANSLATION),
    region=ENDPOINT_REGION,
    timeout=TIMEOUT_SEC
)

_KEYBOARD_INTERRUPT_FLAG: bool = False


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


def translate(
    text: str, from_language: str = LANGUAGE_FROM,
    to_language: str = LANGUAGE_TO
) -> str | None:
    """Translates text from one language to another using Azure Text Translation service.

    Args:
        text (str): The text to be translated.
        from_language (str, optional): The language code of the source text. 
            Defaults to `LANGUAGE_FROM`.
        to_language (str, optional): The language code of the target text. 
            Defaults to `LANGUAGE_TO`.

    Returns:
        str: The translated text, or None if an error occurs.

    Raises:
        Exception: If there is an error during the translation process.

    """
    input_text_elements = [text]
    translation: str | None = None
    try:
        response = CLIENT.translate(
            body=input_text_elements, to_language=[
                to_language], from_language=from_language
        )
        if response:
            translation = response[0].translations[0].text
    except KeyboardInterrupt:
        global _KEYBOARD_INTERRUPT_FLAG  # pylint: disable=global-statement
        _KEYBOARD_INTERRUPT_FLAG = True
    return translation


def translate_from_file(fpath: str, language: str = LANGUAGE_TO) -> str | None:
    """Translates text from a file to a specified language using Azure Text Translation service.

    Args:
        fpath (str): The path to the file containing the text to be translated.
        language (str, optional): The language code of the target text. 
            Defaults to `LANGUAGE_TO`.

    Returns:
        str: The translated text, or None if an error occurs.

    Raises:
        Exception: If there is an error during the translation process or reading the file.

    """
    with open(fpath, "r", encoding="utf-8") as ff:
        return translate(ff.read(), to_language=language)


def translate_from_dir(src: str, language: str = LANGUAGE_TO) -> None:
    """Translates text files from a directory to a specified language
    using Azure Text Translation service.

    This function iterates through all text files (excluding files with extensions
    in `EXCLUDE_SUFFIX`) in the specified directory and translates them
    to the target language using the `translate_from_file` function.
    The translated content is saved in a new file with the original filename appended with
    "_translated.txt". Existing translations are skipped.
    Finally, all translated content is merged into a single file named "translated_merged.txt"
    in the output directory. 

    Args:
        src (str): The path to the directory containing the text files to be translated.
            Raises `ValueError` if the path is not a directory.
        language (str, optional): The language code of the target text. Defaults to `LANGUAGE_TO`.

    Returns:
        None

    Raises:
        ValueError: If the `src` argument is not a directory path.

    **Performance:** This function translates files sequentially. For large directories, consider 
    using asynchronous or parallel processing for better performance.

    **Error Handling:** While the function raises `ValueError` for invalid input paths, it catches 
    other potential exceptions during translation.  Consider adding more specific error handling 
    to provide informative messages to the user.
    """
    global _KEYBOARD_INTERRUPT_FLAG  # pylint: disable=global-statement
    if not os.path.isdir(src):
        raise ValueError("'src' must be a directory path.")
    dstdir: str = os.path.join(src, DEFAULT_OUTPUT_DIRNAME)
    if not os.path.exists(dstdir):
        os.makedirs(dstdir)

    translated_list = []
    filename_list = [
        fname for fname in os.listdir(src)
        if os.path.isfile(os.path.join(src, fname))
    ]
    n_files = len(filename_list)
    print(f"# of files: {n_files}")
    try:
        for ii, fname in enumerate(filename_list):
            print(f"target: {fname} ({ii + 1}/{n_files})")
            if not os.path.isfile(os.path.join(src, fname)):
                continue
            dstpath_target = os.path.join(
                dstdir,
                os.path.basename(fname).replace(
                    os.path.splitext(fname)[-1],
                    "_translated.txt"
                )
            )
            translated: str | None = None
            if os.path.exists(dstpath_target):
                print("already translated.")
                with open(dstpath_target, "r", encoding="utf-8") as ff:
                    translated = ff.read()
                    translated_list.append(translated)
                continue
            if EXCLUDE_SUFFIX in fname:
                print("a file to exclude. skip.")
                continue
            translated = translate_from_file(
                os.path.join(src, fname),
                language
            )
            if _KEYBOARD_INTERRUPT_FLAG:
                print("skip analysis of the rest files due to KeyBoardInterrupt.")
                break
            if translated is None:
                print("failure in translation. skip.")
                continue
            translated_list.append(translated)
            dstpath_target = os.path.join(
                dstdir,
                os.path.basename(fname).replace(
                    os.path.splitext(fname)[-1],
                    "_translated.txt"
                )
            )
            save(dstpath_target, translated)
            print(f"done. wait {WAIT_TIME_SEC} sec...")
            time.sleep(WAIT_TIME_SEC)
    except KeyboardInterrupt:
        _KEYBOARD_INTERRUPT_FLAG = True

    if _KEYBOARD_INTERRUPT_FLAG:
        return
    print("save a merged translated...")
    dstpath_target = os.path.join(
        dstdir, "translated_merged.txt"
    )
    save(dstpath_target, "\n\n".join(translated_list))


def main(fpath: str, language: str = LANGUAGE_TO) -> None:
    """Translates text or text files to a specified language.

    Args:
        fpath (str): The path to the file or directory to be translated.
        language (str, optional): The language code of the target text. Defaults to `LANGUAGE_TO`.

    Raises:
        ValueError: If `fpath` is not a valid file or directory path, or if translation fails.

    This function determines whether `fpath` is a file or a directory. If it's a file,
    it calls `translate_from_file` to translate the text. If it's a directory,
    it calls `translate_from_dir` to recursively translate all text files within the directory.
    The translated text is saved in a new file with the suffix "_translated.txt" in a 
    subdirectory named `DEFAULT_OUTPUT_DIRNAME`.

    **Note:** This function relies on the following functions:
        * `translate_from_file`: Translates a single text file.
        * `translate_from_dir`: Translates all text files in a directory.
        * `save`: Saves the translated text to a file.

    **Error Handling:** Raises a `ValueError` if there is an error during the translation process
    or if the input path is invalid.
    """
    if os.path.isdir(fpath):
        translate_from_dir(fpath, language)
    else:
        translated = translate_from_file(fpath, language)
        if translated is None:
            raise ValueError("failure in translation.")
        dstdir = os.path.join(
            os.path.dirname(fpath), DEFAULT_OUTPUT_DIRNAME
        )
        if not os.path.exists(dstdir):
            os.makedirs(dstdir)
        dstpath_target = os.path.join(
            dstdir,
            os.path.basename(fpath).replace(
                os.path.splitext(fpath)[-1],
                "_translated.txt"
            )
        )
        save(dstpath_target, translated)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("src", type=str)
    parser.add_argument(
        "--la", dest="la", type=str, default=LANGUAGE_TO
    )
    args = parser.parse_args()
    main(args.src, args.la)
