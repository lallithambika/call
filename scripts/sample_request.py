"""Sample script to test API with a local MP3 file."""

import argparse
import base64
import json
from pathlib import Path

import requests


def to_base64(file_path: Path) -> str:
    return base64.b64encode(file_path.read_bytes()).decode("utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", required=True, help="Path to mp3 file")
    parser.add_argument("--url", default="http://localhost:8000/api/call-analytics")
    parser.add_argument("--api-key", default="change-me")
    parser.add_argument("--language", default="Tamil", choices=["Tamil", "Tanglish", "Hindi", "Hinglish"])
    args = parser.parse_args()

    payload = {
        "language": args.language,
        "audioFormat": "mp3",
        "audioBase64": to_base64(Path(args.file)),
    }

    response = requests.post(
        args.url,
        headers={"x-api-key": args.api_key, "Content-Type": "application/json"},
        data=json.dumps(payload),
        timeout=300,
    )
    print(response.status_code)
    print(json.dumps(response.json(), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
