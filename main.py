from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import CORS_ORIGINS
from app.models import ChatRequest, ChatResponse
from app.rag import search_documents, generate_answer, collection

app = FastAPI(
    title="Sujoy Kundu Portfolio RAG API",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {
        "status": "online",
        "service": "Sujoy Kundu Portfolio RAG API",
    }

@app.get("/health")
def health():
    return {
        "status": "healthy",
        "documents": collection.count(),
    }

@app.post("/api/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    documents = search_documents(request.message, request.top_k)
    answer = generate_answer(request.message, documents)

    seen = set()
    sources = []

    for item in documents:
        source = item["source"]
        if source not in seen:
            sources.append({"source": source})
            seen.add(source)

    return {
        "answer": answer,
        "sources": sources,
    }
