from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.core.config import CHUNK_SIZE, CHUNK_OVERLAP


def split_documents(documents: list[dict]) -> list[dict]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP
    )

    chunks = []

    for doc in documents:
        text_chunks = splitter.split_text(doc["content"])

        for i, chunk in enumerate(text_chunks):
            chunks.append(
                {
                    "source": doc["source"],
                    "chunk_index": i,
                    "content": chunk
                }
            )

    return chunks