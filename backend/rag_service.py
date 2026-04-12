from backend.src.loader import load_document
from backend.src.splitter import split_documents
from backend.src.vectorstore import create_vectorstore
from backend.src.rag_chain import create_qa_chain


def answer_question_from_file(file_path: str, question: str):
    """
    Process an uploaded document and answer a question using RAG.
    """

    documents = load_document(file_path)
    docs = split_documents(documents)

    vectorstore = create_vectorstore(docs)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

    qa_chain = create_qa_chain(retriever)
    result = qa_chain.invoke({"query": question})

    sources = []
    for doc in result["source_documents"]:
        sources.append(
            {
                "content": doc.page_content[:700],
                "source": doc.metadata.get("source"),
                "page": doc.metadata.get("page"),
                "chunk_id": doc.metadata.get("chunk_id"),
            }
        )

    return {
        "question": question,
        "answer": result["result"],
        "sources": sources,
    }
    
    
# rag_service.py:
# - Bu faylda document-based question answering üçün əsas RAG pipeline service funksiyası yaradılıb.
# - Məqsəd file processing və retrieval logic-i API route qatından ayırmaqdır.
# - Bu yanaşma backend-i daha modulyar edir və route-ları sadə saxlayır.
# - Eyni service sonradan başqa endpoint-lər və ya background processing üçün də istifadə oluna bilər.


# I extracted the document-grounded QA pipeline into a dedicated RAG service module.
# This separates AI processing logic from HTTP request handling and makes the backend more modular and maintainable.
# It also improves reusability, since the same service can later be used by multiple endpoints.