import os

from ... import BaseClient

try:
    import pyttsx3  # type: ignore
except ImportError:
    pyttsx3 = None

from ...exceptions import ModuleNotInstalled


class SAPIClient(BaseClient):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        if pyttsx3 is None:
            raise ModuleNotInstalled("pyttsx3")

        try:
            self._client = pyttsx3.init("sapi5")
        except ModuleNotFoundError:
            raise ModuleNotInstalled("sapi")

    def synth(self, text: str) -> bytes:
        temp_filename = self.create_temp_filename(".wav")
        self._client.save_to_file(text, temp_filename)
        self._client.runAndWait()

        with open(temp_filename, "rb") as temp_f:
            content = temp_f.read()
        os.remove(temp_filename)
        return content
