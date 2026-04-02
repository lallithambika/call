import json
from abc import ABC, abstractmethod
from openai import OpenAI
from transformers import pipeline

from src.config import get_settings


class BaseLLMClient(ABC):
    @abstractmethod
    def summarize(self, text: str) -> str: ...

    @abstractmethod
    def extract_keywords(self, text: str) -> list[str]: ...


class OpenAIClient(BaseLLMClient):
    def __init__(self) -> None:
        settings = get_settings()
        self.client = OpenAI(api_key=settings.openai_api_key)
        self.model = settings.openai_model

    def _chat(self, prompt: str) -> str:
        response = self.client.responses.create(
            model=self.model,
            input=prompt,
            temperature=0.2,
        )
        return response.output_text.strip()

    def summarize(self, text: str) -> str:
        prompt = (
            "Summarize this call center transcript in 2-3 concise lines. "
            f"Transcript:\n{text}"
        )
        return self._chat(prompt)

    def extract_keywords(self, text: str) -> list[str]:
        prompt = (
            "Extract 8 important business keywords from this transcript. "
            "Return valid JSON array of strings only.\n"
            f"Transcript:\n{text}"
        )
        raw = self._chat(prompt)
        try:
            parsed = json.loads(raw)
            return [str(item) for item in parsed][:8]
        except Exception:
            return [x.strip() for x in raw.split(",") if x.strip()][:8]


class HuggingFaceClient(BaseLLMClient):
    def __init__(self) -> None:
        settings = get_settings()
        self.summarizer = pipeline("summarization", model=settings.hf_summarizer_model)
        self.keyword_generator = pipeline("text-generation", model="google/flan-t5-base")

    def summarize(self, text: str) -> str:
        clipped = text[:3000]
        summary = self.summarizer(clipped, max_length=90, min_length=25, do_sample=False)
        return summary[0]["summary_text"].strip()

    def extract_keywords(self, text: str) -> list[str]:
        prompt = (
            "List the top 8 business keywords from this transcript. "
            "Return as comma-separated words only:\n"
            f"{text[:1500]}"
        )
        output = self.keyword_generator(prompt, max_new_tokens=80, do_sample=False)
        generated = output[0]["generated_text"].split(":")[-1]
        return [x.strip(" .") for x in generated.split(",") if x.strip()][:8]


def get_llm_client() -> BaseLLMClient:
    settings = get_settings()
    if settings.llm_provider == "openai" and settings.openai_api_key:
        return OpenAIClient()
    return HuggingFaceClient()
