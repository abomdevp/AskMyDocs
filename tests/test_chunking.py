from app.core.config import PDF_DIR
from app.services.pdf_loader import load_all_pdfs
from app.services.text_splitter import split_documents


def main():
    documents = load_all_pdfs(PDF_DIR)

    chunks = split_documents(documents)

    print(f"Documentos cargados: {len(documents)}")
    print(f"Chunks generados: {len(chunks)}")
    print("-" * 50)

    for i, chunk in enumerate(chunks[:3]):
        print(f"Chunk {i+1}")
        print(chunk["content"][:200])
        print("-" * 50)


if __name__ == "__main__":
    main()