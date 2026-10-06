from pathlib import Path
from typing import Any

from pypdf import PdfReader


class DocumentExtractionError(Exception):
    """Raised when a document cannot be extracted."""


class DocumentExtractor:
    """
    Extracts text from supported document formats.

    Supported:
    - .txt
    - .md
    - .pdf
    """

    SUPPORTED_EXTENSIONS = {".txt", ".md", ".pdf"}

    def extract(self, file_path: str | Path) -> dict[str, Any]:
        path = Path(file_path)

        if not path.exists():
            raise DocumentExtractionError(
                f"File does not exist: {path}"
            )

        extension = path.suffix.lower()

        if extension not in self.SUPPORTED_EXTENSIONS:
            raise DocumentExtractionError(
                f"Unsupported file type: {extension}"
            )

        if extension in {".txt", ".md"}:
            text = self._extract_text_file(path)

        elif extension == ".pdf":
            text = self._extract_pdf(path)

        else:
            raise DocumentExtractionError(
                f"Unsupported file type: {extension}"
            )

        text = self._clean_text(text)

        if not text:
            raise DocumentExtractionError(
                f"No text could be extracted from: {path.name}"
            )

        return {
            "text": text,
            "metadata": {
                "filename": path.name,
                "file_type": extension.lstrip("."),
                "source": str(path),
            },
        }

    def _extract_text_file(self, path: Path) -> str:
        try:
            return path.read_text(
                encoding="utf-8",
                errors="replace",
            )
        except OSError as exc:
            raise DocumentExtractionError(
                f"Could not read {path.name}: {exc}"
            ) from exc

    def _extract_pdf(self, path: Path) -> str:
        try:
            reader = PdfReader(str(path))

            pages = []

            for page_number, page in enumerate(reader.pages, start=1):
                page_text = page.extract_text() or ""

                if page_text.strip():
                    pages.append(
                        f"[Page {page_number}]\n{page_text}"
                    )

            return "\n\n".join(pages)

        except Exception as exc:
            raise DocumentExtractionError(
                f"Could not extract PDF {path.name}: {exc}"
            ) from exc

    def _clean_text(self, text: str) -> str:
        """
        Basic normalization.

        We intentionally keep this conservative.
        More advanced cleaning will come with the chunking pipeline.
        """

        lines = [line.rstrip() for line in text.splitlines()]

        cleaned_lines = []
        previous_blank = False

        for line in lines:
            is_blank = not line.strip()

            if is_blank:
                if not previous_blank:
                    cleaned_lines.append("")
                previous_blank = True
            else:
                cleaned_lines.append(line.strip())
                previous_blank = False

        return "\n".join(cleaned_lines).strip()