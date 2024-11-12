# utils/tts.py

import os
from gtts import gTTS

class TTSProcessor:
    """
    Class responsible for converting text to speech.
    """

    def text_to_speech(self, text, filename):
        """
        Converts text to speech and saves it as an audio file using gTTS.
        :param text: Text to convert to speech
        :param filename: Original filename to base the audio filename on
        :return: Path to the audio file
        """
        audio_filename = f"{os.path.splitext(filename)[0]}.mp3"
        audio_path = os.path.join('static', 'uploads', audio_filename)

        # Use gTTS for TTS processing
        tts = gTTS(text=text, lang='en')
        tts.save(audio_path)

        return audio_path
