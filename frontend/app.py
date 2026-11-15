
import streamlit as st
import requests
import os

from dotenv import load_dotenv

load_dotenv()

API_URL = os.getenv("API_URL")

st.set_page_config(
    page_title="Multi-Document RAG",
    layout="wide"
)

st.title("Intelligent Multi-Document RAG")
st.caption("Ask questions across multiple PDF documents.")

# Session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "conversation_id" not in st.session_state:
    st.session_state.conversation_id = None

# Sidebar: PDF Upload
with st.sidebar:
    st.header("Document Management")

    uploaded_files = st.file_uploader(
        "Upload PDF documents",
        type=["pdf"],
        accept_multiple_files=True
    )

    if st.button("Process Documents"):
        if uploaded_files:
            files = [
                ("files", (file.name, file.getvalue(), "application/pdf"))
                for file in uploaded_files
            ]

            try:
                response = requests.post(
                    f"{API_URL}/documents/upload",
                    files=files,
                    timeout=300
                )

                                
                if response.ok:
                    result = response.json()

                    st.success("Upload complete!")

                    for item in result["results"]:
                        filename = item["filename"]
                        status = item["status"]

                        if status == "processed":
                            st.success(
                                f"{filename} uploaded!"
                            )

                        elif status == "skipped":
                            st.warning(
                                f"{filename} already exists."
                            )

                        else:
                            st.error(
                                f"{filename} — {item['message']}"
                            )


                else:
                    st.error(response.text)

            except requests.RequestException as e:
                st.error(f"Backend connection failed: {e}")
        else:
            st.warning("Please upload at least one PDF.")



for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

        if message.get("sources"):
            with st.expander("View Sources"):
                for source in message["sources"]:
                    st.write(
                        f"**Document:** {source['document']}"
                    )
                    st.write(f"**Page:** {source['page']}")
                    st.caption(source["content"])



question = st.chat_input("Ask something about your documents...")

if question:
    st.session_state.messages.append({
        "role": "user",
        "content": question
    })

    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        with st.spinner("Searching documents and generating answer..."):

            history = "\n".join(
                f"{msg['role']}: {msg['content']}"
                for msg in st.session_state.messages[:-1]
            )

            try:
                response = requests.post(
                    f"{API_URL}/chat/",
                    json={
                        "question": question,
                        "conversation_id": st.session_state.conversation_id
                    },
                    timeout=120
                )

                response.raise_for_status()
                result = response.json()

                st.session_state.conversation_id = result["conversation_id"]

                answer = result["answer"]
                sources = result.get("sources", [])

                st.markdown(answer)

                if sources:
                    with st.expander("View Sources"):
                        for source in sources:
                            st.write(f"**Document:** {source['document']}")
                            st.write(f"**Page:** {source['page']}")
                            st.caption(source["content"][0:100])

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer,
                    "sources": sources
                })

            except requests.RequestException as e:
                answer = f"Unable to get an answer: {e}"
                st.error(answer)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer,
                    "sources": []
                })
