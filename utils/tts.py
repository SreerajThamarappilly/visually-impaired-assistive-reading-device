import pyttsx3
import os
from gtts import gTTS

class TTSProcessor:
    """
    Class responsible for converting text to speech.
    """

    def __init__(self):
        """
        Initializes the TTSProcessor class.
        """
        # Initialize the TTS engine
        self.engine = pyttsx3.init()
        # Set properties (optional)
        self.engine.setProperty('rate', 150)
        self.engine.setProperty('volume', 1.0)

    def text_to_speech(self, text, filename):
        """
        Converts text to speech and saves it as an audio file.
        :param text: Text to convert to speech
        :param filename: Original filename to base the audio filename on
        :return: Path to the audio file
        """
        audio_filename = f"{os.path.splitext(filename)[0]}.mp3"
        audio_path = os.path.join('static', 'uploads', audio_filename)

        # Use pyttsx3 for offline TTS
        self.engine.save_to_file(text, audio_path)
        self.engine.runAndWait()

        # Alternatively, use gTTS for online TTS (uncomment below)
        # tts = gTTS(text=text, lang='en')
        # tts.save(audio_path)

        return audio_path
