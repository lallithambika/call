import logging
from src.celery_app import celery_app
from src.pipeline import run_pipeline

logger = logging.getLogger(__name__)


@celery_app.task(name="tasks.process_call", bind=True)
def process_call_task(self, language: str, audio_base64: str) -> dict:
    logger.info("Processing call task_id=%s", self.request.id)
    return run_pipeline(language=language, audio_base64=audio_base64)
