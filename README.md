# RAG PDF API

Sistema RAG local para hacer preguntas sobre documentos PDF usando Python, FastAPI, Chroma, Sentence Transformers y Ollama.

## Características

- Carga de PDFs desde carpeta local
- Extracción de texto con `pypdf`
- Chunking con LangChain
- Embeddings locales con `sentence-transformers`
- Base vectorial local con Chroma
- Generación de respuestas con Ollama
- API REST con FastAPI
- Ingesta idempotente para evitar duplicados

## Stack

- Python 3.11
- FastAPI
- Uvicorn
- LangChain Text Splitters
- ChromaDB
- sentence-transformers
- Ollama
- pypdf

## Estructura del proyecto

```text
rag-pdf-api/
├── app/
│   ├── api/
│   ├── core/
│   ├── schemas/
│   ├── services/
│   └── main.py
├── data/
│   ├── chroma/
│   └── pdfs/
├── tests/
├── README.md
└── requirements.txt

## Arquitectura

PDF → Texto → Chunks → Embeddings → Chroma → Retrieval → Ollama → Respuesta

1. Los PDFs se cargan desde una carpeta local.
2. Se extrae el texto del documento.
3. El texto se divide en **chunks**.
4. Cada chunk se convierte en **embeddings**.
5. Los embeddings se almacenan en **ChromaDB**.
6. Cuando el usuario hace una pregunta:
   - se convierte en embedding
   - se buscan los chunks más relevantes
   - se construye un prompt con ese contexto
   - Ollama genera la respuesta.

---

## Stack Tecnológico

- **Python 3.11**
- **FastAPI** (API REST)
- **Uvicorn** (ASGI server)
- **ChromaDB** (Vector Database)
- **Sentence Transformers** (Embeddings)
- **LangChain Text Splitters** (Chunking)
- **pypdf** (Extracción de texto de PDFs)
- **Ollama** (LLM local)

---

## Instalación

Clonar el repositorio y crear el entorno virtual.

```bash
python -m venv .venv
source .venv/Scripts/activate
pip install -r requirements.txt

## Ejecutar la API

python -m uvicorn app.main:app --reload

La API quedará disponible en:

http://127.0.0.1:8000

Documentación interactiva:

http://127.0.0.1:8000/docs

## Endpoints

# POST /ingest

Procesa los PDFs ubicados en:

data/pdfs

Este endpoint:

1. Carga los PDFs
2. Extrae el texto
3. Divide el texto en chunks
4. Genera embeddings
5. Guarda los vectores en ChromaDB

Ejemplo de respuesta:

{
  "documents_loaded": 1,
  "chunks_created": 64,
  "chunks_inserted": 64,
  "chunks_skipped": 0,
  "message": "Ingesta completada correctamente"
}

# POST /ask

Permite hacer preguntas sobre los documentos indexados.

Ejemplo de request:

{
  "question": "¿De qué trata el documento?",
  "n_results": 3
}

Ejemplo de respuesta:

{
  "question": "¿De qué trata el documento?",
  "answer": "El documento describe el patrón general del sueño en la infancia...",
  "context_chunks": [
    "chunk 1...",
    "chunk 2...",
    "chunk 3..."
  ]
}

# POST /reset

Reinicia la colección de ChromaDB.

Este endpoint es útil para desarrollo y pruebas cuando se quiere volver a ingerir los documentos desde cero.

Ejemplo de respuesta:

{
  "message": "Colección reiniciada correctamente"
}

## Flujo de uso

1️⃣ Colocar uno o más PDFs en:

data/pdfs

2️⃣ Ejecutar el endpoint:

POST /ingest

3️⃣ Realizar preguntas usando:

POST /ask

## Ejemplo de uso

Pregunta:

¿De qué trata el documento?

El sistema:

1. Convierte la pregunta en embedding
2. Busca chunks similares en Chroma
3. Construye un prompt con ese contexto
4. Envía el prompt a Ollama
5. Devuelve la respuesta generada# AskMyDocs
