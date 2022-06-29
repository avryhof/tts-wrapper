from typing import Any, List, Optional

from ...exceptions import UnsupportedFileFormat
from ...tts import AbstractTTS, FileFormat
from . import MicrosoftClient, MicrosoftSSML


class MicrosoftTTS(AbstractTTS):
    @classmethod
    def supported_formats(cls) -> List[FileFormat]:
        return ["wav", "mp3"]

    def __init__(
        self,
        client: MicrosoftClient,
        lang: Optional[str] = None,
        voice: Optional[str] = None,
    ) -> None:
        self.client = client
        self.lang = lang or "en-US"
        self.voice = voice or "en-US-JessaNeural"

    def synth_to_bytes(self, text: Any, format: FileFormat) -> bytes:
        if format not in self.supported_formats():
            raise UnsupportedFileFormat(format, self.__class__.__name__)
        return self.client.synth(str(text), format)

    @property
    def ssml(self) -> MicrosoftSSML:
        return MicrosoftSSML(self.lang, self.voice)
