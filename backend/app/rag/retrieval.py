import time

from app.embeddings.embedder import EmbeddingService
from app.vectorstore.chroma_store import ChromaVectorStore


class Retriever:

    def __init__(self):
        self.embedder = EmbeddingService()
        self.store = ChromaVectorStore()

    def retrieve(
        self,
        question: str,
        top_k: int = 5
    ):

        print("\n" + "=" * 80)
        print("RETRIEVAL STARTED")
        print("=" * 80)

        total_start = time.time()

        # -------------------------------------------------
        # Step 1 : Generate Query Embedding
        # -------------------------------------------------

        print("[STEP 1] Generating query embedding...")

        embedding_start = time.time()

        embedding = self.embedder.embed_text(question)

        print(
            f"✓ Embedding generated in "
            f"{time.time() - embedding_start:.2f}s"
        )

        # -------------------------------------------------
        # Step 2 : Search ChromaDB
        # -------------------------------------------------

        print("\n[STEP 2] Searching ChromaDB...")

        search_start = time.time()

        results = self.store.search(
            embedding,
            top_k
        )

        print(
            f"✓ Search completed in "
            f"{time.time() - search_start:.2f}s"
        )

        if not results["documents"]:
            print("No documents found.")
            return []

        docs = results["documents"][0]
        meta = results["metadatas"][0]

        distances = []

        if "distances" in results:
            distances = results["distances"][0]

        retrieved_chunks = []

        print("\nRetrieved Chunks")
        print("-" * 80)

        for i, (doc, metadata) in enumerate(zip(docs, meta)):

            score = None

            if distances:
                score = distances[i]

            retrieved_chunks.append(
                {
                    "text": doc,
                    "document": metadata.get("document"),
                    "page": metadata.get("page"),
                    "score": score
                }
            )

            print(f"Chunk {i + 1}")
            print(f"Document : {metadata.get('document')}")
            print(f"Page     : {metadata.get('page')}")

            if score is not None:
                print(f"Distance : {score:.4f}")

            print()

        print("=" * 80)
        print(
            f"RETRIEVAL COMPLETED "
            f"({time.time() - total_start:.2f}s)"
        )
        print("=" * 80)

        return retrieved_chunks