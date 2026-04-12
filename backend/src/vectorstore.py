import os
from langchain_community.vectorstores import FAISS
from backend.src.embeddings import get_embeddings


def create_vectorstore(docs):
    """
    Create a FAISS vectorstore in memory from document chunks.
    Best for temporary or request-based use cases.
    """

    embeddings = get_embeddings()
    vectorstore = FAISS.from_documents(docs, embeddings)
    return vectorstore


def create_or_load_vectorstore(docs, path="faiss_index"):
    """
    Load an existing FAISS vectorstore from disk if it exists.
    Otherwise, create a new one from document chunks and save it locally.
    Best for persistent knowledge bases.
    """

    embeddings = get_embeddings()

    if os.path.exists(path):
        vectorstore = FAISS.load_local(
            folder_path=path,
            embeddings=embeddings,
            allow_dangerous_deserialization=True,
        )
    else:
        vectorstore = FAISS.from_documents(docs, embeddings)
        vectorstore.save_local(path)

    return vectorstore