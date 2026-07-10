from uuid import uuid4

from langchain_text_splitters import RecursiveCharacterTextSplitter

from .schemas import (
    Document,
    DocumentChunk,
)


class Chunker:

    def __init__(
        self,
        chunk_size: int,
        overlap: int,
    ):

        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=overlap,
            separators=[
                "\n\n",
                "\n",
                ". ",
                " ",
                ""
            ],
        )

    def split(
        self,
        document: Document,
    ):

        pieces = self.splitter.split_text(
            document.text
        )

        chunks = []

        for text in pieces:

            chunks.append(
                DocumentChunk(
                    chunk_id=str(uuid4()),
                    document_name=document.filename,
                    page=0,
                    text=text,
                    metadata=document.metadata,
                )
            )

        return chunks