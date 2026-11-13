
from fastapi import FastAPI

app = FastAPI(
    title="Intelligent Multi-Document RAG System",
    description="A multi-document RAG application for intelligent document question answering.",
    version="1.0.0"
)


@app.get("/")
def root():
    return {
        "message": "Intelligent Multi-Document RAG System API is running!"
    }


@app.get("/home")
def home():
    return {
        "status": "application is working"
    }
