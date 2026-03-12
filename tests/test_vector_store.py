from app.core.config import PDF_DIR
from app.services.pdf_loader import load_all_pdfs
from app.services.text_splitter import split_documents
from app.services.embedding_service import EmbeddingService
from app.services.vector_store import VectorStoreService


def main():
    documents = load_all_pdfs(PDF_DIR)
    chunks = split_documents(documents)

    embedding_service = EmbeddingService()

    texts = [chunk["content"] for chunk in chunks]
    embeddings = embedding_service.embed_documents(texts)

    vector_store = VectorStoreService()
    vector_store.add_documents(chunks, embeddings)

    query = "¿De qué trata el documento?"
    query_embedding = embedding_service.embed_query(query)

    results = vector_store.query(query_embedding, n_results=3)

    print("RESULTADOS:")
    print(results)


if __name__ == "__main__":
    main()