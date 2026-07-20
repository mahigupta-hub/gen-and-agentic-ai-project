import uvicorn
import sys
import os
from dotenv import load_dotenv
load_dotenv()
import shutil
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# -----------------------------------------------------------------------
# 1. PYTHON PATH RESOLUTION
# -----------------------------------------------------------------------
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(CURRENT_DIR)
sys.path.append(ROOT_DIR)

# Import the RAG module
from RAG.rag_module import RAGIndex

# Import your teammate's PDF processing function!
from pdf_processing.processor import process_pdf

# --- NEW: IMPORT AI FEATURES ---
from ai_features.qa import answer_question
from ai_features.summary import generate_summary
from ai_features.quiz import generate_quiz
from ai_features.flashcards import generate_flashcards
from ai_features.study_plan import generate_study_plan

app = FastAPI(title="Academic Tutor API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------------------------------------------------
# 2. INITIALIZE THE RAG ENGINE
# -----------------------------------------------------------------------
RAG_INDEX_PATH = os.path.join(ROOT_DIR, "RAG", "saved_index")
_rag_instance = None

def get_rag():
    global _rag_instance
    if _rag_instance is not None:
        return _rag_instance
    
    print("🧠 Loading RAG Index into memory for the first time...")
    rag = RAGIndex()
    try:
        rag.load(RAG_INDEX_PATH)
        _rag_instance = rag
        return _rag_instance
    except Exception as e:
        print(f"Error loading RAG: {e}")
        return None

# -----------------------------------------------------------------------
# 3. PYDANTIC MODELS FOR REQUESTS
# -----------------------------------------------------------------------
class ChatRequest(BaseModel):
    user_id: str
    message: str

class ChatResponse(BaseModel):
    status: str
    bot_response: str

# Model for endpoints that just need the document text
class DocumentRequest(BaseModel):
    text: str

# Model specifically for the Study Plan endpoint
class StudyPlanRequest(BaseModel):
    topic: str
    days: int
    hours: int

# -----------------------------------------------------------------------
# 4. ENDPOINTS
# -----------------------------------------------------------------------

# --- UPLOAD ENDPOINT ---
@app.post("/upload-pdf")
async def upload_pdf_endpoint(file: UploadFile = File(...)):
    temp_file_path = f"temp_{file.filename}"
    
    try:
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        print(f"📄 Processing PDF: {file.filename}...")
        raw_chunks = process_pdf(temp_file_path)
        
        if not raw_chunks:
            os.remove(temp_file_path)
            return {"status": "error", "message": "No text could be extracted from this PDF."}
        
        extracted_chunks = []
        for i, chunk_data in enumerate(raw_chunks):
            if isinstance(chunk_data, str):
                extracted_chunks.append({
                    "chunk_id": i + 1,
                    "text": chunk_data,
                    "page": 1 
                })
            else:
                extracted_chunks.append(chunk_data)
        
        # --- FIX: GET THE RAG ENGINE SAFELY ---
        # If get_rag() returns None (because index doesn't exist), 
        # we create a fresh RAGIndex() so we can build a new one.
        rag = get_rag() or RAGIndex() 
        
        print("🧠 Building AI Search Index...")
        rag.build_index(extracted_chunks)
        rag.save(RAG_INDEX_PATH)
        
        os.remove(temp_file_path)
        
        return {"status": "success", "message": f"{file.filename} processed and indexed successfully!"}
        
    except Exception as e:
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
        return {"status": "error", "message": f"Failed to process file: {str(e)}"}

# --- CHAT ENDPOINT (INTEGRATED WITH AI) ---
@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    incoming_text = request.message
    
    # 1. FETCH THE RAG ENGINE (This triggers the lazy load)
    rag = get_rag()
    if not rag:
        return ChatResponse(status="error", bot_response="The AI index is not loaded. Please upload a document first.")
    
    try:
        # 2. NOW you can use rag.retrieve safely
        matched_chunks = rag.retrieve(incoming_text, k=3)
        
        if not matched_chunks:
            bot_answer = "I searched the documents but couldn't find any information relevant to your question."
        else:
            context_text = "\n\n".join([c.get('text', '') for c in matched_chunks])
            bot_answer = answer_question(context=context_text, question=incoming_text)
            
    except Exception as e:
        bot_answer = f"The AI encountered an issue processing your request: {str(e)}"
        
    return ChatResponse(
        status="success",
        bot_response=bot_answer
    )

# --- NEW AI FEATURE ENDPOINTS ---

@app.post("/summary")
async def get_summary_endpoint(request: DocumentRequest):
    try:
        ai_result = generate_summary(request.text)
        return {"status": "success", "data": ai_result}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.post("/quiz")
async def get_quiz_endpoint(request: DocumentRequest):
    try:
        ai_result = generate_quiz(request.text)
        return {"status": "success", "data": ai_result}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.post("/flashcards")
async def get_flashcards_endpoint(request: DocumentRequest):
    try:
        ai_result = generate_flashcards(request.text)
        return {"status": "success", "data": ai_result}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.post("/study-plan")
async def get_study_plan_endpoint(request: StudyPlanRequest):
    try:
        # Passes the topic, days, and hours to her study plan function
        ai_result = generate_study_plan(request.topic, request.days, request.hours)
        return {"status": "success", "data": ai_result}
    except Exception as e:
        return {"status": "error", "message": str(e)}
    
if __name__ == "__main__":
    # This allows Render to tell your app which port to use
    port = int(os.environ.get("PORT", 10000)) 
    uvicorn.run(app, host="0.0.0.0", port=port)