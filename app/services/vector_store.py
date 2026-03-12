import chromadb

from app.core.config import CHROMA_DIR, CHROMA_COLLECTION_NAME
from app.core.utils import generate_chunk_id


class VectorStoreService:
    def __init__(self, collection_name: str = CHROMA_COLLECTION_NAME):
        self.client = chromadb.PersistentClient(path=str(CHROMA_DIR))
        self.collection_name = collection_name
        self.collection = self.client.get_or_create_collection(name=collection_name)

    def add_documents(self, chunks: list[dict], embeddings: list[list[float]]):
        ids = [
            generate_chunk_id(
                source=chunk["source"],
                chunk_index=chunk["chunk_index"],
                content=chunk["content"],
            )
            for chunk in chunks
        ]

        documents = [chunk["content"] for chunk in chunks]
        metadatas = [
            {
                "source": chunk["source"],
                "chunk_index": chunk["chunk_index"],
            }
            for chunk in chunks
        ]

        existing = self.collection.get(ids=ids)
        existing_ids = set(existing.get("ids", [])) if existing else set()

        new_ids = []
        new_documents = []
        new_metadatas = []
        new_embeddings = []

        for i, chunk_id in enumerate(ids):
            if chunk_id not in existing_ids:
                new_ids.append(chunk_id)
                new_documents.append(documents[i])
                new_metadatas.append(metadatas[i])
                new_embeddings.append(embeddings[i])

        if new_ids:
            self.collection.add(
                ids=new_ids,
                documents=new_documents,
                metadatas=new_metadatas,
                embeddings=new_embeddings,
            )

        return {
            "requested": len(ids),
            "inserted": len(new_ids),
            "skipped": len(ids) - len(new_ids),
        }

    def query(self, query_embedding: list[float], n_results: int = 3):
        return self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
        )

    def count(self) -> int:
        return self.collection.count()

    def reset_collection(self):
        self.client.delete_collection(name=self.collection_name)
        self.collection = self.client.get_or_create_collection(name=self.collection_name)