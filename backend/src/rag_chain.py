import os
from pydantic import SecretStr

from langchain_openai import ChatOpenAI
from langchain_classic.chains import RetrievalQA
from langchain_core.prompts import PromptTemplate


def create_qa_chain(retriever):
    """
    Create a RetrievalQA chain that combines retriever + LLM
    with a stricter custom prompt for document-grounded answers.
    """

    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise ValueError("OPENROUTER_API_KEY is missing in the .env file.")

    llm = ChatOpenAI(
        model="deepseek/deepseek-chat",
        api_key=SecretStr(api_key),
        base_url="https://openrouter.ai/api/v1",
        temperature=0,
    )

    prompt_template = """
You are an AI assistant for document-based question answering.

Answer the user's question using ONLY the provided context.

Rules:
1. Use only the provided context.
2. Do not use outside knowledge.
3. Do not make up or infer missing facts.
4. If the answer is not explicitly available in the context, reply exactly:
   The answer is not explicitly available in the provided document context.
5. Keep the answer short, clear, and directly relevant to the question.
6. Do not ask follow-up questions.
7. Do not add headings, bullet points, or extra explanation unless the question explicitly asks for them.

Context:
{context}

Question:
{question}

Answer:
"""

    prompt = PromptTemplate(
        template=prompt_template,
        input_variables=["context", "question"],
    )

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True,
        chain_type_kwargs={"prompt": prompt},
    )

    return qa_chain