from pathlib import Path
from pypdf import PdfReader


def load_pdf(file_path: Path) -> str:
    reader = PdfReader(str(file_path))
    text_parts = []

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text_parts.append(page_text)

    return "\n".join(text_parts)


def load_all_pdfs(pdf_dir: Path) -> list[dict]:
    documents = []

    if not pdf_dir.exists():
        return documents

    for pdf_file in pdf_dir.glob("*.pdf"):
        text = load_pdf(pdf_file)

        documents.append(
            {
                "source": pdf_file.name,
                "content": text,
            }
        )

    return documents