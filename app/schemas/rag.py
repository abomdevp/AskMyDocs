from pydantic import BaseModel


class AskRequest(BaseModel):
    question: str
    n_results: int = 3


class AskResponse(BaseModel):
    question: str
    answer: str
    context_chunks: list[str]
    sources: list[str]


class IngestResponse(BaseModel):
    documents_loaded: int
    chunks_created: int
    chunks_inserted: int
    chunks_skipped: int
    message: str


class ResetResponse(BaseModel):
    message: str