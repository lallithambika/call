# Call Center Compliance AI

Production-ready FastAPI service for call center audio analytics in Hindi/Hinglish and Tamil/Tanglish.

## Features

- MP3 Base64 input → Whisper transcription
- LLM-powered summary + keyword extraction
- SOP adherence validation (Greeting, Identification, Problem, Solution, Closing)
- Analytics extraction: payment preference, rejection reason, sentiment
- Async execution with Celery + Redis
- Vector storage for transcripts using ChromaDB (FAISS-compatible ecosystem)
- API-key security and environment-based config
- Docker + docker-compose setup

## Project Structure

```text
src/
  main.py
  config.py
  celery_app.py
  pipeline.py
  tasks.py
  schemas.py
  stt/
  nlp/
  analytics/
  sop/
  utils/
  vector_store/
tests/
requirements.txt
README.md
.env.example
Dockerfile
docker-compose.yml
```

## Setup (Local)

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Run API:

```bash
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

Run worker:

```bash
celery -A src.tasks worker --loglevel=info
```

## Setup (Docker)

```bash
docker compose up --build
```

## API

`POST /api/call-analytics`

Headers:

- `x-api-key: <value from X_API_KEY>`

Request body:

```json
{
  "language": "Tamil",
  "audioFormat": "mp3",
  "audioBase64": "..."
}
```

Response body (strict):

```json
{
  "status": "success",
  "language": "Tamil",
  "transcript": "...",
  "summary": "...",
  "sop_validation": {
    "greeting": true,
    "identification": false,
    "problemStatement": true,
    "solutionOffering": true,
    "closing": true,
    "complianceScore": 0.8,
    "adherenceStatus": "NOT_FOLLOWED",
    "explanation": "..."
  },
  "analytics": {
    "paymentPreference": "PARTIAL_PAYMENT",
    "rejectionReason": "BUDGET_CONSTRAINTS",
    "sentiment": "Neutral"
  },
  "keywords": ["..."]
}
```

## Sample Client Script

```bash
python scripts/sample_request.py --file ./sample.mp3 --api-key change-me --language Tamil
```

## Notes

- For OpenAI-based NLP, set `LLM_PROVIDER=openai` and provide `OPENAI_API_KEY`.
- For HuggingFace-only execution, keep `LLM_PROVIDER=huggingface`.
- Whisper and transformer models are large; first run will download model weights.
