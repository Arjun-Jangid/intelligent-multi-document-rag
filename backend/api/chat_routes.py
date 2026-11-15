
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from backend.database.database import get_db
from backend.database.models import Conversation
from backend.services.conversation_service import (
    create_conversation,
    save_message,
    get_conversation_history
)

from backend.services.retrieval import retrieve_documents
from backend.services.llm import (
    generate_answer,
    contextualize_question
)


router = APIRouter(prefix="/chat", tags=["Chat"])


class ChatRequest(BaseModel):
    question: str
    conversation_id: int | None = None


@router.post("/")
def chat(
    request: ChatRequest,
    db: Session = Depends(get_db)
):

    if not request.question.strip():
        raise HTTPException(400, "Question cannot be empty.")


    if request.conversation_id is None:
        conversation = create_conversation(db)
    else:
        conversation = db.query(Conversation).filter(
            Conversation.id == request.conversation_id
        ).first()

        if not conversation:
            raise HTTPException(404, "Conversation not found.")

    conversation_id = conversation.id

    try:
        history = get_conversation_history(db, conversation_id)

        chat_history = "\n".join(
            f"{message['role']}: {message['content']}"
            for message in history
        )


        save_message(
            db,
            conversation_id,
            "user",
            request.question
        )


        standalone_question = contextualize_question(
            question=request.question,
            chat_history=chat_history
        )

        print()
        print("Original Question:", request.question)
        print("Standalone Question:", standalone_question)


        chunks = retrieve_documents(standalone_question)

        answer = generate_answer(
            question=request.question,
            retrieved_chunks=chunks,
            chat_history=chat_history
        )


        save_message(
            db,
            conversation_id,
            "assistant",
            answer
        )


        sources = [
            {
                "document": chunk["metadata"]["source"],
                "page": chunk["metadata"]["page"],
                "content": chunk["text"]
            }
            for chunk in chunks
        ]

        return {
            "conversation_id": conversation_id,
            "question": request.question,
            "answer": answer,
            "sources": sources
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Unable to generate answer: {str(e)}"
        )
