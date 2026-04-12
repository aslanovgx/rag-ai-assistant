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
    chain = get_llm_chain()
    response = chain.invoke({"input": request.message})

    return {
        "reply": response.content
    }


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

    finally:
        if os.path.exists(temp_path):
            os.unlink(temp_path)

# main.py:
# - Bu fayl FastAPI backend-in entry point-idir.
# - Burada API server yaradılır və əsas endpoint-lər təyin olunur.
# - "/" endpoint sadə test üçün istifadə olunur.
# - "/health" endpoint isə serverin işlək vəziyyətdə olub olmadığını yoxlamaq üçün istifadə olunur.
# - Bu, production sistemlərdə monitoring və deployment üçün vacibdir.


# /chat endpoint:
# - Bu endpoint general chatbot funksionallığı üçün yaradılıb.
# - İstifadəçidən sadəcə bir message qəbul edir və onu birbaşa LLM-ə göndərir.
# - Bu mərhələdə retrieval və document grounding yoxdur.
# - Məqsəd əvvəlcə backend-də basic conversational AI endpoint qurmaq idi.
# - Sonrakı mərhələdə bunun yanına file-based RAG endpoint əlavə olunacaq.


# /upload endpoint: 
# - Bu endpoint backend-in fayl qəbul edə bildiyini yoxlamaq üçün əlavə olunub.
# - FastAPI-də fayl upload etmək üçün UploadFile və File istifadə olunur.
# - Bu, sonrakı RAG pipeline üçün ilk addımdır, çünki document-based Q&A sistemi əvvəlcə istifadəçinin göndərdiyi faylı qəbul etməlidir.


# /ask-file endpoint:
# - Bu endpoint document-grounded question answering üçün yaradılıb.
# - İstifadəçidən həm fayl, həm də sual qəbul edir.
# - Fayl əvvəlcə backend-də müvəqqəti saxlanılır.
# - Sonra unified loader ilə oxunur, chunk-lara bölünür və vectorstore yaradılır.
# - Retriever və LLM birlikdə istifadə edilərək suala sənədə əsaslanan cavab qaytarılır.
# - Response daxilində source chunks da verilir ki cavabın hansı hissələrə əsaslandığı görünsün.


# This response shows the full retrieval-plus-generation flow.
# The query was embedded, the retriever selected the top 3 semantically relevant chunks, and the LLM generated a grounded summary based on those chunks.
# The strongest source was the chunk defining the Enterprise Architecture Framework, while the other chunks reinforced the document’s practical and transitional context.


# I initially used a persistent vectorstore approach for all retrieval flows,
# but then I separated the architecture by use case.

# For file-based question answering, I switched to an in-memory vectorstore,
# because each uploaded document is temporary and request-specific.

# A persistent create-or-load strategy is more suitable for long-lived knowledge bases,
# such as company documents or website content.


# save_uploaded_temp_file():
# - Bu helper funksiya upload olunan faylın yoxlanılması və müvəqqəti saxlanılması üçün yazılıb.
# - Məqsəd eyni upload logic-in fərqli endpoint-lərdə təkrarlanmamasıdır.
# - Bu refactor kodu daha təmiz, daha maintainable və daha reusable edir.

# Refactor:
# - /chat endpoint içindəki LLM initialization logic çıxarılıb.
# - Bunun əvəzinə backend/llm_service.py içində get_llm() funksiyası yaradılıb.
# - Bu yanaşma route layer-i daha təmiz saxlayır və model konfiqurasiyasını mərkəzləşdirir.
# - Əgər gələcəkdə model, provider və ya temperature dəyişsə, yalnız service qatında dəyişiklik etmək kifayət edəcək.