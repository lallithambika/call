from transformers import pipeline
from src.config import get_settings


class AnalyticsExtractor:
    def __init__(self) -> None:
        settings = get_settings()
        self.zero_shot = pipeline("zero-shot-classification", model=settings.hf_zero_shot_model)
        self.sentiment = pipeline("sentiment-analysis", model=settings.hf_sentiment_model)

    def _classify(self, transcript: str, labels: list[str]) -> str:
        result = self.zero_shot(transcript[:2500], candidate_labels=labels, multi_label=False)
        return result["labels"][0]

    def extract(self, transcript: str) -> dict:
        payment_preference = self._classify(
            transcript,
            ["EMI", "FULL_PAYMENT", "PARTIAL_PAYMENT", "DOWN_PAYMENT"],
        )
        rejection_reason = self._classify(
            transcript,
            [
                "HIGH_INTEREST",
                "BUDGET_CONSTRAINTS",
                "ALREADY_PAID",
                "NOT_INTERESTED",
                "NONE",
            ],
        )
        raw_sentiment = self.sentiment(transcript[:500])[0]["label"].lower()
        sentiment_map = {
            "positive": "Positive",
            "neutral": "Neutral",
            "negative": "Negative",
            "label_0": "Negative",
            "label_1": "Neutral",
            "label_2": "Positive",
        }

        return {
            "paymentPreference": payment_preference,
            "rejectionReason": rejection_reason,
            "sentiment": sentiment_map.get(raw_sentiment, "Neutral"),
        }
