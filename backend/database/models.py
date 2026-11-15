from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Text

from backend.database.database import Base

from sqlalchemy.orm import relationship

class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False, default="New Conversation")
    created_at = Column(DateTime, nullable=False)

    messages = relationship(
        "Message",
        back_populates="conversation",
        cascade="all, delete-orphan"
    )


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id"), nullable=False)
    role = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, nullable=False)

    conversation = relationship("Conversation", back_populates="messages")


