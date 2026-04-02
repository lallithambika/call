import logging
from celery.result import AsyncResult
from fastapi import Depends, FastAPI, HTTPException

from src.config import get_settings
from src.schemas import CallAnalyticsRequest, CallAnalyticsResponse
from src.tasks import process_call_task
from src.utils.logging import configure_logging
from src.utils.security import validate_api_key

configure_logging()
logger = logging.getLogger(__name__)
settings = get_settings()

app = FastAPI(title=settings.app_name, version="1.0.0")


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/api/call-analytics", response_model=CallAnalyticsResponse)
def call_analytics(
    payload: CallAnalyticsRequest,
    _: str = Depends(validate_api_key),
) -> CallAnalyticsResponse:
    """Accept audio payload and return strict call analytics JSON."""
    if payload.audioFormat != "mp3":
        raise HTTPException(status_code=400, detail="Only mp3 format is supported")

    task = process_call_task.delay(payload.language, payload.audioBase64)
    result = AsyncResult(task.id)

    try:
        response = result.get(timeout=settings.task_timeout_seconds)
    except Exception as exc:
        logger.exception("Failed call analytics task_id=%s", task.id)
        raise HTTPException(status_code=500, detail="Failed to process call analytics") from exc

    return CallAnalyticsResponse(**response)
