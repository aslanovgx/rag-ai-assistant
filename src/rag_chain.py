import os
from pydantic import SecretStr

# from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI
from langchain_classic.chains import RetrievalQA


def create_qa_chain(retriever):
    """
    Create RetrievalQA chain that combines retriever + LLM.
    """

    # llm = ChatOpenAI(
    #     model="gpt-4o-mini",
    #     temperature=0 # çox olsa, daha creative or random cavablar verir, az olsa daha deterministic cavablar verir, bizə lazım olan budur
    # )
    
    
    # llm = ChatOllama(
    #     model="llama3",
    #     temperature=0
    # )
    
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise ValueError("OPENROUTER_API_KEY is missing in the .env file.")

    llm = ChatOpenAI(
        model="deepseek/deepseek-chat",
        api_key=SecretStr(api_key) if api_key else None,
        base_url="https://openrouter.ai/api/v1",
        temperature=0,
    )

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff", # tapılan hissələri yığıb bir yerdə modelə verir || It means the retrieved documents are concatenated together and passed to the LLM as a single context block.
        retriever=retriever,
        return_source_documents=True # To make the system more transparent and debuggable by showing which retrieved chunks were used to generate the answer.
    )

    return qa_chain