from src.nlp.llm_client import get_llm_client


class NLPProcessor:
    def __init__(self) -> None:
        self.client = get_llm_client()

    def summarize(self, transcript: str) -> str:
        return self.client.summarize(transcript)

    def keywords(self, transcript: str) -> list[str]:
        return self.client.extract_keywords(transcript)
