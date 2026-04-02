import chromadb
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction
from src.config import get_settings


class TranscriptVectorStore:
    def __init__(self) -> None:
        settings = get_settings()
        self.client = chromadb.PersistentClient(path=settings.chroma_persist_directory)
        self.collection = self.client.get_or_create_collection(
            name="call_transcripts",
            embedding_function=SentenceTransformerEmbeddingFunction(
                model_name=settings.embedding_model
            ),
        )

    def store(self, call_id: str, transcript: str, metadata: dict) -> None:
        self.collection.upsert(
            ids=[call_id],
            documents=[transcript],
            metadatas=[metadata],
        )
