from app.services.rag_service import RAGService


def main():
    rag_service = RAGService(model_name="llama3.2")

    question = "¿De qué trata el documento?"

    result = rag_service.answer_question(question)

    print("PREGUNTA:")
    print(result["question"])
    print("-" * 50)

    print("CHUNKS RECUPERADOS:")
    for i, chunk in enumerate(result["context_chunks"], start=1):
        print(f"\nChunk {i}:")
        print(chunk[:500])

    print("\n" + "-" * 50)
    print("RESPUESTA:")
    print(result["answer"])


if __name__ == "__main__":
    main()