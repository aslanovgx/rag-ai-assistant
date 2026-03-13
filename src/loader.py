from langchain_community.document_loaders import PyPDFLoader
from src.text_cleaner import clean_text


def load_pdf(file_path: str):
    """
    Load a PDF file and convert it into LangChain Document objects.
    """

    loader = PyPDFLoader(file_path)
    documents = loader.load()
    
    # text cleaning for each document
    for doc in documents:
        doc.page_content = clean_text(doc.page_content)

    return documents