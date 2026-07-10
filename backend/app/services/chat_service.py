import time

from app.llm.groq_service import GroqService
from app.rag.prompt import SYSTEM_PROMPT
from app.rag.retrieval import Retriever


class ChatService:

    MAX_HISTORY = 10

    def __init__(self):

        self.retriever = Retriever()

        self.llm = GroqService()

        self.history = []

    def ask(
        self,
        question: str
    ):

        print("\n" + "=" * 80)
        print("CHAT REQUEST")
        print("=" * 80)

        total_start = time.time()

        print(f"Question : {question}")

        # -------------------------------------------------------
        # Step 1 : Retrieve Context
        # -------------------------------------------------------

        retrieval_start = time.time()

        retrieved_chunks = self.retriever.retrieve(question)

        print(
            f"\n✓ Retrieval Time : "
            f"{time.time() - retrieval_start:.2f}s"
        )

        if not retrieved_chunks:

            return {
                "answer": "No relevant information found in the uploaded documents.",
                "sources": []
            }

        # -------------------------------------------------------
        # Step 2 : Build Context
        # -------------------------------------------------------

        context = "\n\n".join(
            chunk["text"]
            for chunk in retrieved_chunks
        )

        history = "\n".join(self.history)

        prompt = SYSTEM_PROMPT.format(
            context=context,
            history=history,
            question=question
        )

        # -------------------------------------------------------
        # Step 3 : Generate Answer
        # -------------------------------------------------------

        print("\nGenerating LLM response...")

        llm_start = time.time()

        answer = self.llm.generate(prompt)

        print(
            f"✓ LLM Time : "
            f"{time.time() - llm_start:.2f}s"
        )

        # -------------------------------------------------------
        # Step 4 : Maintain Chat History
        # -------------------------------------------------------

        self.history.extend([
            f"User: {question}",
            f"Assistant: {answer}"
        ])

        if len(self.history) > self.MAX_HISTORY:
            self.history = self.history[-self.MAX_HISTORY:]

        # -------------------------------------------------------
        # Step 5 : Prepare Sources
        # -------------------------------------------------------

        seen = set()
        sources = []

        for chunk in retrieved_chunks:

            key = (
                chunk["document"],
                chunk["page"]
            )

            if key not in seen:

                seen.add(key)

                sources.append(
                    {
                        "document": chunk["document"],
                        "page": chunk["page"]
                    }
                )

        print(
            f"\n✓ Total Chat Time : "
            f"{time.time() - total_start:.2f}s"
        )

        print("=" * 80)

        return {
            "answer": answer,
            "sources": sources
        }

    def clear_history(self):

        self.history = []