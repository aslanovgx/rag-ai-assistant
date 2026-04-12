# src/splitter.py
from langchain_text_splitters import RecursiveCharacterTextSplitter


def split_documents(documents):
    """
    Split documents into smaller chunks while preserving metadata.
    """

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=700,
        chunk_overlap=100,
    )

    docs = splitter.split_documents(documents)

    # propagate chunk-level metadata
    for i, doc in enumerate(docs):
        doc.metadata["chunk_id"] = i

    return docs


# split_documents():
# - Bu funksiya document-ləri kiçik chunk-lara bölür.
# - Chunking RAG üçün vacibdir, çünki LLM-ə bütün sənəd yox, uyğun hissələr verilir.
# - chunk_size və overlap context balansını qorumaq üçün seçilir.
# - Hər chunk-a chunk_id əlavə olunur ki sonradan izləmək mümkün olsun.

# I use a recursive text splitter to break documents into manageable chunks.
# This improves retrieval accuracy, as only the most relevant segments are passed to the LLM.
# I also attach a chunk_id to each segment for better traceability and debugging.