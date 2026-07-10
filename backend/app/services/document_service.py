from pathlib import Path
import time
import traceback

from app.core.config import settings
from app.ingestion.loader import DocumentLoader
from app.ingestion.chunker import Chunker
from app.embeddings.embedder import EmbeddingService
from app.vectorstore.chroma_store import ChromaVectorStore


class DocumentService:

    def __init__(self):

        print("=" * 80)
        print("Initializing DocumentService...")

        self.loader = DocumentLoader()
        print("✓ DocumentLoader initialized")

        self.chunker = Chunker(
            settings.CHUNK_SIZE,
            settings.CHUNK_OVERLAP
        )
        print("✓ Chunker initialized")

        self.embedder = EmbeddingService()
        print("✓ EmbeddingService initialized")

        self.store = ChromaVectorStore()
        print("✓ ChromaVectorStore initialized")

        print("DocumentService Ready")
        print("=" * 80)

    def ingest(self, file_path: Path):

        total_start = time.time()

        print("\n")
        print("=" * 80)
        print("DOCUMENT INGESTION STARTED")
        print("=" * 80)

        try:

            # -------------------------------------------------------
            # STEP 1
            # -------------------------------------------------------
            print("\n[STEP 1] Loading document...")

            start = time.time()

            document = self.loader.load(file_path)

            print(f"✓ Loaded in {time.time()-start:.2f}s")
            print(f"Filename : {document.filename}")
            print(f"Characters : {len(document.text)}")

            if len(document.text.strip()) == 0:
                raise Exception("Document contains no text.")

            # -------------------------------------------------------
            # STEP 2
            # -------------------------------------------------------
            print("\n[STEP 2] Checking duplicate...")

            start = time.time()

            exists = self.store.document_exists(
                document.filename
            )

            print(f"✓ Duplicate Check : {exists}")
            print(f"Time : {time.time()-start:.2f}s")

            if exists:
                print("Document already exists in ChromaDB.")
                return 0

            # -------------------------------------------------------
            # STEP 3
            # -------------------------------------------------------
            print("\n[STEP 3] Chunking document...")

            start = time.time()

            chunks = self.chunker.split(document)

            print(f"✓ Chunking completed in {time.time()-start:.2f}s")
            print(f"Total Chunks : {len(chunks)}")

            if len(chunks) == 0:
                raise Exception("Chunker returned zero chunks.")

            # -------------------------------------------------------
            # STEP 4
            # -------------------------------------------------------
            print("\n[STEP 4] Generating embeddings...")

            start = time.time()

            texts = [chunk.text for chunk in chunks]

            embeddings = self.embedder.embed_batch(texts)

            print(f"✓ Embeddings generated in {time.time()-start:.2f}s")
            print(f"Embeddings Returned : {len(embeddings)}")

            if len(embeddings) != len(chunks):
                raise Exception(
                    f"Embedding count mismatch. "
                    f"Chunks={len(chunks)}, "
                    f"Embeddings={len(embeddings)}"
                )

            # -------------------------------------------------------
            # STEP 5
            # -------------------------------------------------------
            print("\n[STEP 5] Saving into ChromaDB...")

            start = time.time()

            self.store.add_chunks(
                chunks,
                embeddings
            )

            print(f"✓ Saved in {time.time()-start:.2f}s")

            # -------------------------------------------------------
            print("\n")
            print("=" * 80)
            print("DOCUMENT INGESTION SUCCESS")
            print(f"TOTAL TIME : {time.time()-total_start:.2f}s")
            print("=" * 80)

            return len(chunks)

        except Exception as e:

            print("\n")
            print("=" * 80)
            print("DOCUMENT INGESTION FAILED")
            print("=" * 80)

            print(f"Error Type : {type(e).__name__}")
            print(f"Error : {e}")

            print("\nTraceback:\n")
            traceback.print_exc()

            print("=" * 80)

            raise