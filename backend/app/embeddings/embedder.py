import requests

from app.core.config import settings


class EmbeddingService:

    def __init__(self):
        self.url = "https://api.jina.ai/v1/embeddings"

        self.headers = {
            "Authorization": f"Bearer {settings.JINA_API_KEY}",
            "Content-Type": "application/json"
        }

    def embed_text(self, text: str):

        payload = {
            "model": "jina-embeddings-v3",
            "input": [text]
        }

        response = requests.post(
            self.url,
            headers=self.headers,
            json=payload,
            timeout=60
        )

        response.raise_for_status()

        return response.json()["data"][0]["embedding"]

    def embed_batch(self, texts):

        payload = {
            "model": "jina-embeddings-v3",
            "input": texts
        }

        response = requests.post(
            self.url,
            headers=self.headers,
            json=payload,
            timeout=120
        )

        response.raise_for_status()

        return [
            item["embedding"]
            for item in response.json()["data"]
        ]