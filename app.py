import os
import streamlit as st
from dotenv import load_dotenv

from src.loader import load_pdf
from src.splitter import split_documents
from src.vectorstore import create_vectorstore
from src.rag_chain import create_qa_chain
from src.utils import save_uploaded_file

load_dotenv()

st.set_page_config(page_title="RAG AI Assistant", page_icon="📄")
st.title("📄 RAG AI Assistant")
st.write("PDF yüklə və sənəddən sual soruş.")

uploaded_file = st.file_uploader("PDF faylını seç", type=["pdf"])

if uploaded_file is not None:

    tmp_path = save_uploaded_file(uploaded_file)

    documents = load_pdf(tmp_path)
    docs = split_documents(documents)

    vectorstore = create_vectorstore(docs)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

    qa_chain = create_qa_chain(retriever)

    query = st.text_input("Sualını yaz")

    if query:

        result = qa_chain.invoke({"query": query})

        st.subheader("Cavab")
        st.write(result["result"])

        st.subheader("İstifadə olunan hissələr")

        for i, doc in enumerate(result["source_documents"], 1):
            st.markdown(f"**Chunk {i}:**")
            st.write(doc.page_content[:700])
            st.markdown("---")

    os.unlink(tmp_path)