# 📄 RAG AI Assistant

A simple **Retrieval-Augmented Generation (RAG)** application that allows users to upload a PDF and ask questions about its content.

---

## 🚀 Features

* 📥 Upload PDF documents
* ✂️ Automatic text chunking
* 🔍 Semantic search using vector embeddings
* 🧠 Context-aware answers using LLM
* 📚 Source chunk transparency (see where answers come from)

---

## 🧠 How It Works

1. Upload a PDF file
2. The system:

   * Loads and cleans the text
   * Splits it into smaller chunks
   * Converts chunks into vector embeddings
   * Stores them in a FAISS vector database
3. When a question is asked:

   * The system retrieves the most relevant chunks
   * Passes them to the LLM
   * Generates a context-aware answer

---

## 🏗️ Project Structure

```
rag-ai-assistant/
│
├── app.py                 # Streamlit UI
├── requirements.txt
├── .env
├── README.md
│
├── src/
│   ├── loader.py          # PDF loading
│   ├── splitter.py        # Text chunking
│   ├── embeddings.py      # Embedding model
│   ├── vectorstore.py     # FAISS database
│   ├── rag_chain.py       # LLM + Retrieval logic
│   ├── utils.py           # File handling
│   └── text_cleaner.py    # Text preprocessing
│
└── data/
```

---

## ⚙️ Installation

```bash
git clone https://github.com/aslanovgx/rag-ai-assistant.git
cd rag-ai-assistant

pip install -r requirements.txt
```

---

## 🔑 Environment Variables

Create a `.env` file:

```
OPENROUTER_API_KEY=your_api_key_here
```

---

## ▶️ Run the App

```bash
streamlit run app.py
```

Then open:

```
http://localhost:8501
```

---

## 🧪 Example Questions

* What is artificial intelligence?
* What are the types of machine learning?
* Explain neural networks in simple terms
* What challenges does AI face?

---

## 🛠️ Tech Stack

* Python
* Streamlit
* LangChain
* FAISS
* OpenRouter (LLM API)
* HuggingFace / OpenAI Embeddings

---

## 📌 Notes

* Chunk size optimized to **700 / 100 overlap** for better retrieval
* Uses **semantic search** instead of keyword search
* Designed as an MVP for RAG systems

---

## 🎯 Future Improvements

* Persistent vector database (no reprocessing on every upload)
* Multi-document support
* Chat history memory
* Better UI/UX
* Streaming responses

---

## 👨‍💻 Author

**Mustafa Aslanov**

* GitHub: https://github.com/aslanovgx
* Portfolio: https://portfolio-website-bay-iota-74.vercel.app

---

## ⭐ If you like this project, give it a star!
