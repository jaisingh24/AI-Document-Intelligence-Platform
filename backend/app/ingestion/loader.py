import fitz
from pathlib import Path

from .schemas import Document


SUPPORTED_EXTENSIONS = {
    ".pdf",
    ".txt",
    ".md"
}


class DocumentLoader:

    def load(self, file_path: Path) -> Document:

        if not file_path.exists():
            raise FileNotFoundError(file_path)

        suffix = file_path.suffix.lower()

        if suffix not in SUPPORTED_EXTENSIONS:
            raise ValueError(
                f"Unsupported file type: {suffix}"
            )

        if suffix == ".pdf":
            return self._load_pdf(file_path)

        return self._load_text(file_path)

    def _load_pdf(self, path: Path) -> Document:

        pdf = fitz.open(path)

        pages = []

        for page in pdf:
            pages.append(page.get_text())

        text = "\n".join(pages)

        pdf.close()

        return Document(
            filename=path.name,
            text=text,
            metadata={
                "source": path.name,
                "pages": len(pages),
                "type": "pdf"
            }
        )

    def _load_text(self, path: Path) -> Document:

        text = path.read_text(
            encoding="utf-8",
            errors="ignore"
        )

        return Document(
            filename=path.name,
            text=text,
            metadata={
                "source": path.name,
                "pages": 1,
                "type": "text"
            }
        )