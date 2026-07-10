from typing import List

import chromadb
from chromadb.config import Settings

from app.core.config import settings
from app.ingestion.schemas import DocumentChunk


class ChromaVectorStore:

    def __init__(self):
        print("Initializing ChromaDB...")

        self.client = chromadb.PersistentClient(
            path=str(settings.CHROMA_DB),
            settings=Settings(
                anonymized_telemetry=False
            )
        )

        self.collection = self.client.get_or_create_collection(
            name="documents",
            metadata={
                "hnsw:space": "cosine"
            }
        )

        print("✓ ChromaDB Ready")

    def add_chunks(self, chunks: List[DocumentChunk], embeddings: List[List[float]]):

        ids = []
        docs = []
        metadatas = []

        for chunk in chunks:
            ids.append(chunk.chunk_id)
            docs.append(chunk.text)

            metadatas.append({
                "document": chunk.document_name,
                "page": chunk.page
            })

        self.collection.add(
            ids=ids,
            documents=docs,
            embeddings=embeddings,
            metadatas=metadatas
        )

        print("✓ Chunks Saved")

    def search(self, embedding, top_k=5):

        return self.collection.query(
            query_embeddings=[embedding],
            n_results=top_k
        )

    def document_exists(self, filename: str):

        result = self.collection.get(
            where={"document": filename}
        )

        return len(result["ids"]) > 0

    def delete_document(self, filename: str):

        self.collection.delete(
            where={"document": filename}
        )

    def count(self):
        return self.collection.count()

    def reset(self):

        self.client.delete_collection("documents")

        self.collection = self.client.create_collection(
            name="documents",
            metadata={
                "hnsw:space": "cosine"
            }
        )