from fastapi import FastAPI

from backend.api.document_routes import router as document_router
from backend.api.chat_routes import router as chat_router

from backend.database.database import Base, engine

app = FastAPI(
    title="Intelligent Multi-Document RAG System",
    version="1.0.0"
)

app.include_router(document_router)
app.include_router(chat_router)

Base.metadata.create_all(bind=engine)


@app.get("/")
def root():
    return {"message": "RAG API is running"}


@app.get("/health")
def health():
    return {"status": "healthy"}