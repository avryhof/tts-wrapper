import pyttsx as pyttsx
from tts_wrapper.tts import TTS


class PyTTSX3(TTS):
    """ A TTS-Wrapper compatible module for pyttsx3"""
    engine = pyttsx.init()

    def __init__(self, voice_name=None, lang=None, rate=175) -> None:
        super().__init__(voice_name=voice_name, lang=lang)

        voices = self.engine.getProperty("voices")
        for voice in list(voices):
            if self.lang.lower() in voice.id:
                self.engine.setProperty("voice", voice.id)

        self.engine.setProperty('rate', rate)  # setting up new voice rate

    def _synth(self, ssml: str, filename=None) -> None:
        """SSML will actually be stripped"""
        if filename is not None:
            self.engine.save_to_file(ssml, filename)
        else:
            self.engine.say(ssml)
        self.engine.runAndWait()
