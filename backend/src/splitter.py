# src/splitter.py
from langchain_text_splitters import RecursiveCharacterTextSplitter


def split_documents(documents):
    """
    Split documents into smaller chunks while preserving metadata.
    """

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=700,
        chunk_overlap=100,
    )

    docs = splitter.split_documents(documents)

    # propagate chunk-level metadata
    for i, doc in enumerate(docs):
        doc.metadata["chunk_id"] = i

    return docs