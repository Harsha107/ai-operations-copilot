import pyttsx3
import speech_recognition as sr
from typing import Optional

class VoiceHandler:
    """Handles voice input and output."""

    def __init__(self):
        """Initialize the voice handler."""
        self.engine = pyttsx3.init()
        self.recognizer = sr.Recognizer()

    def text_to_speech(self, text: str):
        """Convert text to speech."""
        self.engine.say(text)
        self.engine.runAndWait()

    def speech_to_text(self) -> Optional[str]:
        """Convert speech to text."""
        with sr.Microphone() as source:
            print("Listening...")
            audio = self.recognizer.listen(source)

            try:
                text = self.recognizer.recognize_google(audio)
                print(f"Recognized: {text}")
                return text
            except sr.UnknownValueError:
                print("Could not understand audio")
                return None
            except sr.RequestError as e:
                print(f"Error with the speech recognition service; {e}")
                return None