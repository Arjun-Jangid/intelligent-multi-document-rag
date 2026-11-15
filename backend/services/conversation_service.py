
from datetime import datetime, timezone

from sqlalchemy.orm import Session

from backend.database.models import Conversation, Message


def create_conversation(db: Session):

    conversation = Conversation(
        title="New Conversation",
        created_at=datetime.now(timezone.utc)
    )

    db.add(conversation)
    db.commit()
    db.refresh(conversation)

    return conversation


def save_message(
    db: Session,
    conversation_id: int,
    role: str,
    content: str
):

    message = Message(
        conversation_id=conversation_id,
        role=role,
        content=content,
        created_at=datetime.now(timezone.utc)
    )

    db.add(message)
    db.commit()
    db.refresh(message)

    return message


def get_conversation_history(
    db: Session,
    conversation_id: int
):

    messages = (
        db.query(Message)
        .filter(Message.conversation_id == conversation_id)
        .order_by(Message.created_at.asc(), Message.id.asc())
        .all()
    )

    return [
        {
            "role": message.role,
            "content": message.content
        }
        for message in messages
    ]
