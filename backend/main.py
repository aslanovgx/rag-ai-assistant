import os

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from pydantic import BaseModel

from backend.llm_service import get_llm_chain
from backend.rag_service import answer_question_from_file
from backend.file_service import save_uploaded_temp_file
from backend.cors_config import setup_cors

load_dotenv()

app = FastAPI()

setup_cors(app)


class ChatRequest(BaseModel):
    message: str



@app.get("/")
def root():
    return {"message": "RAG AI Assistant API is running 🚀"}


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/chat")
def chat(request: ChatRequest):
    try:
        chain = get_llm_chain()
        response = chain.invoke({"input": request.message})

        if hasattr(response, "content"):
            reply = response.content
        else:
            reply = str(response)

        return {"reply": reply}

    except Exception as e:
        print("CHAT ERROR:", repr(e))
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/upload")
def upload_file(file: UploadFile = File(...)):
    filename, extension, temp_path = save_uploaded_temp_file(file)

    return {
        "filename": filename,
        "content_type": file.content_type,
        "extension": extension,
        "temp_path": temp_path
    }
    
    
    
@app.post("/ask-file")
def ask_file(file: UploadFile = File(...), question: str = Form(...)):
    filename, extension, temp_path = save_uploaded_temp_file(file)

    try:
        result = answer_question_from_file(temp_path, question)
        result["filename"] = filename
        return result

    except Exception as e:
        print("ASK-FILE ERROR:", repr(e))
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        if os.path.exists(temp_path):
            os.unlink(temp_path)