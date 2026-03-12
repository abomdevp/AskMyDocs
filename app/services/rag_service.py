import ollama

from app.core.config import DEFAULT_N_RESULTS, OLLAMA_MODEL_NAME, OLLAMA_HOST
from app.services.embedding_service import EmbeddingService
from app.services.vector_store import VectorStoreService


class RAGService:
    def __init__(self, model_name: str = OLLAMA_MODEL_NAME):
        self.model_name = model_name
        self.embedding_service = EmbeddingService()
        self.vector_store = VectorStoreService()
        self.ollama_client = ollama.Client(host=OLLAMA_HOST)

    def retrieve_context(self, question: str, n_results: int = DEFAULT_N_RESULTS) -> dict:
        query_embedding = self.embedding_service.embed_query(question)
        results = self.vector_store.query(query_embedding, n_results=n_results)

        documents = results.get("documents", [])
        metadatas = results.get("metadatas", [])

        if not documents:
            return {
                "documents": [],
                "metadatas": [],
            }

        return {
            "documents": documents[0],
            "metadatas": metadatas[0] if metadatas else [],
        }

    def build_prompt(self, question: str, context_chunks: list[str]) -> str:
        context_text = "\n\n".join(context_chunks)

        prompt = f"""
Eres un asistente que responde preguntas usando solo el contexto proporcionado.

Si la respuesta no está en el contexto, responde exactamente:
No encontré esa información en los documentos proporcionados.

Responde de forma clara y breve.

Contexto:
{context_text}

Pregunta:
{question}

Respuesta:
""".strip()

        return prompt

    def build_sources(self, metadatas: list[dict]) -> list[str]:
        sources = []

        for metadata in metadatas:
            source = metadata.get("source", "desconocido")
            chunk_index = metadata.get("chunk_index", "N/A")
            sources.append(f"{source} (chunk {chunk_index})")

        return list(dict.fromkeys(sources))

    def answer_question(self, question: str, n_results: int = DEFAULT_N_RESULTS) -> dict:
        retrieval_result = self.retrieve_context(question, n_results=n_results)

        context_chunks = retrieval_result["documents"]
        metadatas = retrieval_result["metadatas"]

        prompt = self.build_prompt(question, context_chunks)

        response = self.ollama_client.chat(
            model=self.model_name,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        )

        sources = self.build_sources(metadatas)

        return {
            "question": question,
            "context_chunks": context_chunks,
            "sources": sources,
            "answer": response["message"]["content"],
        }