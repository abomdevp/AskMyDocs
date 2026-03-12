from fastapi import APIRouter, HTTPException

from app.schemas.rag import AskRequest, AskResponse, IngestResponse, ResetResponse
from app.services.ingestion_service import IngestionService
from app.services.rag_service import RAGService
from app.services.vector_store import VectorStoreService

router = APIRouter()


@router.get("/")
def root():
    return {
        "message": "RAG PDF API running",
        "status": "ok"
    }


@router.get("/health")
def health():
    return {
        "status": "healthy"
    }


@router.post("/ingest", response_model=IngestResponse)
def ingest_documents():
    try:
        ingestion_service = IngestionService()
        result = ingestion_service.ingest()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/ask", response_model=AskResponse)
def ask_question(request: AskRequest):
    try:
        rag_service = RAGService()
        result = rag_service.answer_question(
            question=request.question,
            n_results=request.n_results
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/reset", response_model=ResetResponse)
def reset_vector_store():
    try:
        vector_store = VectorStoreService()
        vector_store.reset_collection()
        return {"message": "Colección reiniciada correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))