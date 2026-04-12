# RAG AI Assistant

A full-stack AI assistant that supports both general chatbot interaction and document-grounded question answering using a Retrieval-Augmented Generation (RAG) pipeline.

The system allows users to upload PDF and DOCX files and ask questions based on their content, returning grounded answers along with relevant source chunks.

---

## 🚀 Features

- General chatbot endpoint powered by an LLM
- Document-based Q&A using RAG
- PDF and DOCX file upload support
- Text cleaning and chunking pipeline
- Semantic search using embeddings + FAISS
- Grounded answers with source traceability
- Custom prompt to reduce hallucination
- Clean backend architecture with service separation

---

## 🧠 Tech Stack

### Backend
- FastAPI
- Python
- LangChain
- FAISS (vector search)
- OpenRouter (LLM access)
- HuggingFace Embeddings

### AI / Retrieval
- `sentence-transformers/all-MiniLM-L6-v2`
- RetrievalQA chain
- Custom prompt engineering
- In-memory vectorstore (request-based RAG)

---

## 🏗️ Project Structure

```bash
backend/
├── main.py              # API routes
├── llm_service.py       # LLM initialization
├── rag_service.py       # RAG pipeline logic
└── file_service.py      # File validation & temp storage

src/
├── loader.py            # PDF/DOCX loading
├── splitter.py          # Text chunking
├── embeddings.py        # Embedding model
├── vectorstore.py       # FAISS handling
├── rag_chain.py         # RetrievalQA + prompt
├── text_cleaner.py      # Text preprocessing
└── utils.py


🔌 API Endpoints

GET /

Check if the API is running.

GET /health

Health check endpoint.

POST /chat

General chatbot endpoint using LLM.

POST /upload

Upload and validate a PDF or DOCX file.

POST /ask-file

Ask a question about an uploaded document using RAG.

⸻

⚙️ How It Works

General Chat

User message → LLM → response

File Chat (RAG)
	1.	File upload
	2.	Document parsing (PDF/DOCX)
	3.	Text cleaning
	4.	Chunking
	5.	Embedding generation
	6.	FAISS vector search
	7.	Relevant chunk retrieval
	8.	LLM generates grounded answer
	9.	Sources returned with response

⸻

▶️ Running the Backend

Install dependencies:
pip install -r requirements.txt

Run the server:
uvicorn backend.main:app --reload

Open Swagger UI:
http://localhost:8000/docs

🧩 Key Design Decisions
	•	Used RAG instead of raw LLM to handle large documents efficiently
	•	Separated backend into service layers (LLM, RAG, file handling)
	•	Implemented in-memory vectorstore for request-based document processing
	•	Added custom prompt to enforce grounded answers and reduce hallucination

⸻

🚧 Future Improvements
	•	User authentication system
	•	Persistent vector database (e.g. Pinecone, Weaviate)
	•	Multi-user document isolation
	•	Voice input support
	•	Frontend UI (Next.js)

⸻

📌 Notes
	•	Version 1 does not include authentication
	•	Supports PDF and DOCX formats
	•	Designed as a modular and extensible AI system