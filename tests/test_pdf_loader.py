from app.core.config import PDF_DIR
from app.services.pdf_loader import load_all_pdfs


def main():
    documents = load_all_pdfs(PDF_DIR)

    print(f"PDF_DIR: {PDF_DIR}")
    print(f"Documentos encontrados: {len(documents)}")
    print("-" * 50)

    for doc in documents:
        print(f"Archivo: {doc['source']}")
        print(f"Largo del texto: {len(doc['content'])}")
        print("Preview:")
        print(doc["content"][:300])
        print("-" * 50)


if __name__ == "__main__":
    main()