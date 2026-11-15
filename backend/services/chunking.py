
from langchain_text_splitters import RecursiveCharacterTextSplitter


def split_documents(pages, source_name):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        separators=["\n\n", "\n", ". ", " ", ""]
    )

    chunks = []

    for page in pages:
        page_chunks = splitter.split_text(page["text"])

        for chunk in page_chunks:
            chunks.append({
                "text": chunk,
                "metadata": {
                    "source": source_name,
                    "page": page["page"]
                }
            })

    return chunks
