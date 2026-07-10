from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class Document:
    """
    Represents one uploaded document.
    """
    filename: str
    text: str
    metadata: Dict[str, Any]


@dataclass
class DocumentChunk:
    """
    Represents one chunk of a document.
    """
    chunk_id: str
    document_name: str
    page: int
    text: str
    metadata: Dict[str, Any]