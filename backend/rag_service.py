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