import pyttsx3  # type: ignore
import os

from ...exceptions import ModuleNotInstalled
from ..utils import create_temp_filename


class SAPIClient:
    def __init__(self) -> None:
        try:
            self._client = pyttsx3.init("sapi5")
        except ModuleNotFoundError:
            raise ModuleNotInstalled("sapi")

    def synth(self, text: str) -> bytes:
        temp_filename = create_temp_filename(".wav")
        self._client.save_to_file(text, temp_filename)
        self._client.runAndWait()

        with open(temp_filename, "rb") as temp_f:
            content = temp_f.read()
        os.remove(temp_filename)
        return content
