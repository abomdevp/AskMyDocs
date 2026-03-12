from app.core.config import PDF_DIR
from app.services.pdf_loader import load_all_pdfs
from app.services.text_splitter import split_documents
from app.services.embedding_service import EmbeddingService


def main():
    documents = load_all_pdfs(PDF_DIR)
    chunks = split_documents(documents)

    texts = [chunk["content"] for chunk in chunks[:3]]

    embedding_service = EmbeddingService()
    vectors = embedding_service.embed_documents(texts)

    print(f"Chunks usados: {len(texts)}")
    print(f"Embeddings generados: {len(vectors)}")
    print(f"Dimensión del vector: {len(vectors[0])}")


if __name__ == "__main__":
    main()