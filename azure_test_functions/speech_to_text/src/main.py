"""speech_to_text"""

import os
import time
from typing import Dict, List, Type, Union
from typing_extensions import TypeAlias
from azure.cognitiveservices.speech import (
    SpeechConfig, AudioConfig, SpeechRecognizer,
    SpeechRecognitionResult, SpeechRecognitionEventArgs,
    ResultReason
)
from mutagen.mp3 import MP3
from mutagen.wave import WAVE

MUTAGEN_ANALYZER_TYPE: TypeAlias = MP3 | WAVE
MUTAGEN_ANALYZER_DICT: Dict[str, Union[Type[MP3], Type[WAVE]]] = {
    "mp3": MP3,
    "wav": WAVE
}

AUDIO_DURATION_SEC_DEFAULT: float = 120.0
TIMEOUT_SEC: float = 30.0
WAIT_TIME_SEC: float = 3.0
LANGUAGE: str = "ja-JP"
DEFAULT_OUTPUT_DIRNAME: str = "transcribed"

KEY_SPEECH: str | None = os.environ.get("AZURE_SPEECH_KEY", None)
ENDPOINT_BASE: str | None = os.environ.get("AZURE_SPEECH_ENDPOINT", None)
ENDPOINT_REGION: str| None = os.environ.get("AZURE_SPEECH_ENDPOINT_REGION", None)

SPEECH_CONFIG = SpeechConfig(
    subscription=KEY_SPEECH, region=ENDPOINT_REGION,
    speech_recognition_language=LANGUAGE
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


def analyze(fpath: str) -> str:
    """Analyzes an audio file and returns a list of speech recognition results.

    This function performs continuous speech recognition on the specified audio file
    and returns a list of `SpeechRecognitionResult` objects. The recognition process
    is timed based on the duration of the audio file.

    Args:
        fpath: The path to the audio file.

    Returns:
        A list of `SpeechRecognitionResult` objects containing the recognized text.
    """
    audio_config = AudioConfig(filename=fpath)
    speech_recognizer = SpeechRecognizer(
        speech_config=SPEECH_CONFIG, audio_config=audio_config
    )
    results: List[SpeechRecognitionResult] = []

    audio_duration_sec: float = AUDIO_DURATION_SEC_DEFAULT
    mutagen_analyzer = MUTAGEN_ANALYZER_DICT.get(
        os.path.splitext(fpath)[-1][1:], None)
    if mutagen_analyzer is not None:
        audio: MUTAGEN_ANALYZER_TYPE = mutagen_analyzer(fpath)
        if audio.info is not None:
            audio_duration_sec = audio.info.length

    def continuous_recognition_handler(evt: SpeechRecognitionEventArgs) -> None:
        nonlocal results
        if evt.result.reason == ResultReason.RecognizedSpeech:
            results.append(evt.result.text)

    try:
        speech_recognizer.recognized.connect(continuous_recognition_handler)
        speech_recognizer.start_continuous_recognition()
        previous_length: int = 0
        st = time.time()
        while time.time() < st + audio_duration_sec:
            time.sleep(1.0)
            if previous_length == 0:
                continue
            if previous_length == len(results):
                break
            previous_length = len(results)
        speech_recognizer.stop_continuous_recognition()
    except KeyboardInterrupt:
        global _KEYBOARD_INTERRUPT_FLAG  # pylint: disable=global-statement
        _KEYBOARD_INTERRUPT_FLAG = True
        print("keyboard interrupt. stop the current recognition...")
        speech_recognizer.stop_continuous_recognition()

    return " ".join(results)


def analyze_from_dir(src: str) -> None:
    """Analyzes images in a directory and saves results as JSON files.

    This function iterates over image files in the specified directory, analyzes each image
    using the `analyze` function, and saves the analysis results as JSON files in a designated
    output directory.

    Args:
        src (str): The path to the directory containing image files.

    Raises:
        NotADirectoryError: If the provided `src` is not a directory.
    """
    global _KEYBOARD_INTERRUPT_FLAG  # pylint: disable=global-statement
    if not os.path.isdir(src):
        raise NotADirectoryError("'src' must be a directory path.")
    dstdir: str = os.path.join(src, DEFAULT_OUTPUT_DIRNAME)
    if not os.path.exists(dstdir):
        os.makedirs(dstdir)

    analyzed_list = []
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
                    ".txt"
                )
            )
            if os.path.exists(dstpath_target):
                print("already analyzed. skip")
                with open(dstpath_target, "r", encoding="utf-8") as ff:
                    analyzed_list.append(ff.read())
                continue
            analyzed = analyze(os.path.join(src, fname))
            if _KEYBOARD_INTERRUPT_FLAG:
                print("skip analysis of the rest files due to KeyBoardInterrupt.")
                break
            if not analyzed:
                print("failure in analysis. skip.")
                time.sleep(WAIT_TIME_SEC)
                continue
            analyzed_list.append(analyzed)
            save(dstpath_target, analyzed)
            print("done.")
            time.sleep(WAIT_TIME_SEC)
    except KeyboardInterrupt:
        _KEYBOARD_INTERRUPT_FLAG = True

    if _KEYBOARD_INTERRUPT_FLAG:
        return
    print("save a merged transcript...")
    dstpath_target = os.path.join(
        dstdir, "transcript_merged.txt"
    )
    save(dstpath_target, "\n\n".join(analyzed_list))


def main(file_or_dir_path: str) -> None:
    """Analyzes an audio file or directory and saves the analysis results as JSON.

    This function recursively analyzes all audio files within the specified directory
    or analyzes the specified audio file. The analysis results for each audio file
    are saved as a separate JSON file in a subdirectory named 'results' within the
    same directory as the input file.

    Args:
        file_or_dir_path: The path to an audio file or directory. Supported audio formats are
               WAV and MP3.

    Raises:
        ValueError: If the specified path is invalid or if the analysis fails.
        OSError: If an error occurs during file operations.
    """
    if os.path.isdir(file_or_dir_path):
        analyze_from_dir(file_or_dir_path)
    else:
        print("analyze...")
        analyzed = analyze(file_or_dir_path)
        if not analyzed:
            raise ValueError("failure in analysis.")
        dstdir = os.path.join(
            os.path.dirname(file_or_dir_path), DEFAULT_OUTPUT_DIRNAME
        )
        if not os.path.exists(dstdir):
            os.makedirs(dstdir)
        dstpath = os.path.join(
            dstdir,
            os.path.basename(file_or_dir_path).replace(
                os.path.splitext(file_or_dir_path)[-1],
                ".txt"
            )
        )
        print("finished. save...")
        save(dstpath, analyzed)
        print("done.")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("src", type=str)
    parser.add_argument(
        "--same_level", dest="same_level", action="store_true"
    )
    args = parser.parse_args()
    main(args.src)
