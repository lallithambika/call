from pathlib import Path
import whisper
from src.config import get_settings


class WhisperTranscriber:
    def __init__(self) -> None:
        settings = get_settings()
        self.model = whisper.load_model(settings.whisper_model)

    def transcribe(self, audio_path: Path, language: str) -> str:
        lang_map = {
            "Hindi": "hi",
            "Hinglish": "hi",
            "Tamil": "ta",
            "Tanglish": "ta",
        }
        result = self.model.transcribe(str(audio_path), language=lang_map.get(language, "en"))
        return result["text"].strip()
