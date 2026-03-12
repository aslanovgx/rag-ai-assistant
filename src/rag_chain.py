from langchain_openai import ChatOpenAI
from langchain_classic.chains import RetrievalQA


def create_qa_chain(retriever):
    """
    Create RetrievalQA chain that combines retriever + LLM.
    """

    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0
    )

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True
    )

    return qa_chain