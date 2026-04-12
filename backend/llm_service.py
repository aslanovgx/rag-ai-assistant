import os
from pydantic import SecretStr
from fastapi import HTTPException
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate


def get_llm_chain():
    """
    Create a general-purpose chat LLM with a controlled prompt.
    """

    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise HTTPException(
            status_code=500,
            detail="OPENROUTER_API_KEY is missing."
        )

    llm = ChatOpenAI(
        model="deepseek/deepseek-chat",
        api_key=SecretStr(api_key),
        base_url="https://openrouter.ai/api/v1",
        temperature=0,
    )

    prompt = ChatPromptTemplate.from_messages([
        ("system", """
You are a helpful AI assistant.

Rules:
- Give clear and concise answers.
- Avoid unnecessary long explanations.
- Do not ask follow-up questions.
- If the question is simple, answer in 1-3 sentences.
- Be direct and helpful.
"""),
        ("human", "{input}")
    ])

    chain = prompt | llm

    return chain