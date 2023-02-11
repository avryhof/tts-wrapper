from abc import ABC, abstractmethod
from typing import Any, List, Literal, Optional, Union

from tts_wrapper import SynthError

FileFormat = Union[Literal["wav"], Literal["mp3"]]


class AbstractTTS(ABC):
    """Abstract class (ABC) used by other text-to-speech classes."""

    @classmethod
    @abstractmethod
    def supported_formats(cls) -> List[FileFormat]:
        """Returns list of supported audio types in concrete text-to-speech classes."""

        pass

    @abstractmethod
    def synth_to_bytes(self, text: Any, format: FileFormat) -> bytes:
        """Transforms written text to audio bytes on supported formats.

        @param text: Text to be transformed into audio bytes
        @param format: File format to be used when transforming to audio bytes, if supported
        @returns: audio bytes created
        @raises UnsupportedFileFormat: if file format is not supported
        """

        pass

    def synth_to_file(
        self, text: Any, filename: str, format: Optional[FileFormat] = None
    ) -> None:
        """Transforms written text to an audio file and saves on disk.

        @param text: Text to be transformed to audio file
        @param filename: Name of the file to be saved on disk
        @param format: File format to be used when transforming to audio file. Defaults to None.
        """

        audio_content = self.synth_to_bytes(text, format=format or "wav")
        with open(filename, "wb") as wav:
            wav.write(audio_content)

    def _synth(self, ssml: str, filename=None) -> None:
        raise NotImplementedError()

    def synth(self, ssml: str, filename=None) -> None:
        """
        @param ssml: the ssml text to synthesize without the speak tag (will be added automatically).
        @param filename: the output wave file path.
        """
        wrapped_ssml = self._wrap_ssml(ssml)
        try:
            self._synth(wrapped_ssml, filename)
        except Exception as e:
            raise SynthError(
                f'Error while calling synth with "{(ssml[:100] + "...") if len(ssml) > 100 else ssml}"'
            ) from e
