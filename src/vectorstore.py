from langchain_community.vectorstores import FAISS
from src.embeddings import get_embeddings


def create_vectorstore(docs):
    """
    Create FAISS vector database from document chunks.
    """

    embeddings = get_embeddings()

    vectorstore = FAISS.from_documents(docs, embeddings)

    return vectorstore