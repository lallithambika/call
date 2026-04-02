from transformers import pipeline
from src.config import get_settings


class SOPValidator:
    def __init__(self) -> None:
        settings = get_settings()
        self.classifier = pipeline("zero-shot-classification", model=settings.hf_zero_shot_model)

    def _present(self, text: str, label: str) -> bool:
        result = self.classifier(
            sequences=text[:2500],
            candidate_labels=[f"contains {label}", f"does not contain {label}"],
            multi_label=False,
        )
        return result["labels"][0].startswith("contains")

    def validate(self, transcript: str) -> dict:
        checks = {
            "greeting": self._present(transcript, "greeting"),
            "identification": self._present(transcript, "agent identification"),
            "problemStatement": self._present(transcript, "customer problem statement"),
            "solutionOffering": self._present(transcript, "solution offering"),
            "closing": self._present(transcript, "closing statement"),
        }
        score = round(sum(checks.values()) / len(checks), 2)
        followed = score >= 0.85
        checks.update(
            {
                "complianceScore": score,
                "adherenceStatus": "FOLLOWED" if followed else "NOT_FOLLOWED",
                "explanation": (
                    "All mandatory SOP stages are mostly present in the transcript."
                    if followed
                    else "One or more mandatory SOP stages are missing or weakly represented."
                ),
            }
        )
        return checks
