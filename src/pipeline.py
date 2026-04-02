import logging
import uuid
from pathlib import Path

from src.analytics.extractor import AnalyticsExtractor
from src.nlp.processor import NLPProcessor
from src.sop.validator import SOPValidator
from src.stt.whisper_service import WhisperTranscriber
from src.utils.audio import decode_base64_to_mp3
from src.vector_store.store import TranscriptVectorStore

logger = logging.getLogger(__name__)


def run_pipeline(language: str, audio_base64: str) -> dict:
    audio_path: Path | None = None
    try:
        audio_path = decode_base64_to_mp3(audio_base64)
        transcript = WhisperTranscriber().transcribe(audio_path=audio_path, language=language)
        nlp = NLPProcessor()
        summary = nlp.summarize(transcript)
        keywords = nlp.keywords(transcript)

        sop_validation = SOPValidator().validate(transcript)
        analytics = AnalyticsExtractor().extract(transcript)

        call_id = str(uuid.uuid4())
        TranscriptVectorStore().store(
            call_id=call_id,
            transcript=transcript,
            metadata={"language": language, "status": "processed"},
        )

        return {
            "status": "success",
            "language": language,
            "transcript": transcript,
            "summary": summary,
            "sop_validation": sop_validation,
            "analytics": analytics,
            "keywords": keywords,
        }
    finally:
        if audio_path and audio_path.exists():
            audio_path.unlink(missing_ok=True)
