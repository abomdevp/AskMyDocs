from app.core.config import PDF_DIR
from app.services.pdf_loader import load_all_pdfs
from app.services.text_splitter import split_documents
from app.services.embedding_service import EmbeddingService
from app.services.vector_store import VectorStoreService


class IngestionService:
    def __init__(self):
        self.embedding_service = EmbeddingService()
        self.vector_store = VectorStoreService()

    def ingest(self) -> dict:
        documents = load_all_pdfs(PDF_DIR)
        chunks = split_documents(documents)

        if not documents:
            return {
                "documents_loaded": 0,
                "chunks_created": 0,
                "chunks_inserted": 0,
                "chunks_skipped": 0,
                "message": "No se encontraron PDFs para ingerir"
            }

        texts = [chunk["content"] for chunk in chunks]
        embeddings = self.embedding_service.embed_documents(texts)

        db_result = self.vector_store.add_documents(chunks, embeddings)

        return {
            "documents_loaded": len(documents),
            "chunks_created": len(chunks),
            "chunks_inserted": db_result["inserted"],
            "chunks_skipped": db_result["skipped"],
            "message": "Ingesta completada correctamente"
        }