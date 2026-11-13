
import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="Multi-Document RAG",
    layout="wide"
)

st.title("Intelligent Multi-Document RAG System")
st.write("Upload multiple PDF documents and ask questions about their contents.")

try:
    response = requests.get(f"{API_URL}/home")
    if response.status_code == 200:
        st.success("Backend connected successfully!")
except requests.exceptions.RequestException:
    st.error("Backend is not running.")
