from celery import Celery
from src.config import get_settings

settings = get_settings()

celery_app = Celery(
    "call_center_compliance_ai",
    broker=settings.celery_broker_url,
    backend=settings.celery_result_backend,
)

celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    task_track_started=True,
    timezone="UTC",
    enable_utc=True,
)
