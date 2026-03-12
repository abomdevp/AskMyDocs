# AskMyDocs

Sistema **RAG (Retrieval Augmented Generation)** para consultar documentos PDF utilizando **FastAPI, ChromaDB y Ollama**.

El sistema permite cargar documentos PDF, indexarlos mediante embeddings y realizar preguntas sobre su contenido utilizando un **modelo de lenguaje ejecutado localmente**.

# Características

- Consulta inteligente de documentos PDF
- Pipeline RAG completo
- Embeddings locales con `sentence-transformers`
- Base vectorial con **ChromaDB**
- Generación de respuestas con **Ollama**
- API REST construida con **FastAPI**
- Ingesta idempotente (evita duplicados)
- Citas de fuente en las respuestas
- Dockerización del proyecto

# Arquitectura

Pipeline del sistema:
PDF --> Texto --> Chunks --> Embeddings --> Chroma --> Retrieval --> Ollama --> Respuesta

# Flujo del sistema:

1. Los PDFs se cargan desde una carpeta local.
2. Se extrae el texto usando `pypdf`.
3. El texto se divide en **chunks**.
4. Cada chunk se convierte en **embeddings vectoriales**.
5. Los embeddings se almacenan en **ChromaDB**.
6. Cuando el usuario hace una pregunta:
   - se convierte en embedding
   - se buscan los chunks más relevantes
   - se construye un prompt con ese contexto
   - Ollama genera la respuesta.

# Stack Tecnológico

- Python 3.11
- FastAPI
- Uvicorn
- ChromaDB
- Sentence Transformers
- LangChain Text Splitters
- pypdf
- Ollama
- Docker

# Instalación

Clonar el repositorio y crear un entorno virtual.

```bash
python -m venv .venv
source .venv/Scripts/activate
pip install -r requirements.txt
```

# Ejecutar la API

```bash
python -m uvicorn app.main:app --reload
```

La API estará disponible en:

http://127.0.0.1:8000

Documentación interactiva (Swagger):

http://127.0.0.1:8000/docs

# Endpoint - POST /ingest

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

# Endpoint - POST /ask

Permite hacer preguntas sobre los documentos indexados.

Ejemplo de request:

{
  "question": "¿De qué trata el documento?",
  "n_results": 3
}

# Endpoint - POST /reset

Reinicia la colección de ChromaDB.

Ejemplo de respuesta:

{
  "message": "Colección reiniciada correctamente"
}

# Ejemplo de uso

Pregunta:

¿De qué trata el documento?

El sistema:

Convierte la pregunta en embedding

Busca chunks similares en Chroma

Construye un prompt con ese contexto

Envía el prompt a Ollama

Devuelve la respuesta generada

# Ejecutar con Docker

Asegúrate de tener Docker Desktop y Ollama ejecutándose localmente.

Construir y levantar la API:

```bash
docker compose up --build
```
