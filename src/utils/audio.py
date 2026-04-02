import base64
import tempfile
from pathlib import Path


class AudioDecodeError(ValueError):
    """Raised when audio payload is invalid."""


def decode_base64_to_mp3(audio_b64: str) -> Path:
    try:
        audio_bytes = base64.b64decode(audio_b64, validate=True)
    except Exception as exc:
        raise AudioDecodeError("Invalid base64 audio payload") from exc

    if len(audio_bytes) == 0:
        raise AudioDecodeError("Audio payload is empty")

    tmp = tempfile.NamedTemporaryFile(suffix=".mp3", delete=False)
    tmp.write(audio_bytes)
    tmp.flush()
    tmp.close()
    return Path(tmp.name)
