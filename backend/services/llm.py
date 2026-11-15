
import os

from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

llm_rewrite = ChatGroq(
    model=os.getenv("GROQ_REWRITE_MODEL"),
    temperature=0
)

llm_answer = ChatGroq(
    model=os.getenv("GROQ_ANSWER_MODEL"),
    temperature=0
)


def generate_answer(question, retrieved_chunks, chat_history=""):

    if not retrieved_chunks:
        return "I couldn't find relevant information in the uploaded documents."

    context = ""

    for chunk in retrieved_chunks:
        metadata = chunk["metadata"]

        context += f"""
Source: {metadata['source']}
Page: {metadata['page']}
Content: {chunk['text']}

"""

    prompt = f"""
You are an intelligent document question-answering assistant.

Answer the user's question using ONLY the provided document context.

Rules:
1. Do not invent information.
2. If the answer is unavailable in the context,
   clearly state that the uploaded documents do not contain
   sufficient information.
3. Use conversational history only to understand follow-up questions.
4. Keep answers clear and relevant.

Conversation History:
{chat_history}

Document Context:
{context}

User Question:
{question}

Answer:
"""

    response = llm_answer.invoke(prompt)

    return response.content




def contextualize_question(question: str, chat_history: str = ""):
    if not chat_history.strip():
        return question

    prompt = f"""
Rewrite the latest user question into a standalone question using the conversation history.

Rules:
- Resolve references such as "it", "its", "that" and "previous year".
- Preserve the user's original intent.
- Do not answer the question.
- Do not add information that isn't present in the history.
- If the question is already standalone, return it unchanged.
- Return ONLY the rewritten standalone question.
- Do not include explanations, labels, or quotation marks.

Conversation History:
{chat_history}

Latest Question:
{question}

Standalone Question:
"""

    response = llm_rewrite.invoke(prompt)

    return response.content.strip()
