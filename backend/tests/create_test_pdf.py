from pathlib import Path

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


output = Path(__file__).parent / "fixtures" / "documents" / "sample.pdf"

pdf = canvas.Canvas(str(output), pagesize=letter)

pdf.setFont("Helvetica", 16)
pdf.drawString(72, 730, "KnowledgeForge Document")

pdf.setFont("Helvetica", 11)

lines = [
    "KnowledgeForge is an enterprise RAG knowledge platform.",
    "",
    "Documents are extracted, chunked, embedded,",
    "and stored in Qdrant for semantic retrieval.",
    "",
    "The platform uses FastAPI, Sentence Transformers,",
    "Qdrant, Ollama, and local language models.",
]

y = 700

for line in lines:
    pdf.drawString(72, y, line)
    y -= 20

pdf.save()

print(f"Created: {output}")