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


# vectorstore.py:
# - Bu faylda FAISS vectorstore yaratmaq üçün iki ayrı yanaşma saxlanılıb.
# - create_vectorstore() request-based və temporary istifadə üçündür.
# - create_or_load_vectorstore() isə persistent knowledge base üçün nəzərdə tutulub.
# - Bu fərqləndirmə ona görə vacibdir ki, bütün use-case-lər eyni storage strategiyasına ehtiyac duymur.
# - Per-file document chat üçün in-memory vectorstore daha uyğundur, sabit knowledge base üçün isə persistence daha məntiqlidir.


# Initially, my RAG pipeline recreated the FAISS index on every run, which was inefficient.
# I refactored the vectorstore layer to support persistence:
# if the index already exists, it is loaded from disk; otherwise, it is created and saved.
# This makes the system faster and closer to a production-style architecture.


# I separated the vectorstore layer into two strategies:
# one for temporary in-memory retrieval, and one for persistent disk-backed retrieval.
# This was important because request-based file Q&A and long-lived knowledge bases have different architectural needs.
# It helped me align the retrieval strategy with the actual use case.