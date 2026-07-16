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

# NEW: Import your teammate's PDF processing function!
from pdf_processing.processor import process_pdf

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
rag = RAGIndex()

try:
    rag.load(RAG_INDEX_PATH)
    print("🚀 SUCCESS: RAG Index loaded perfectly into Backend!")
except Exception as e:
    print(f"⚠️ WARNING: Could not load RAG index: {e}")
    print("This is normal if no PDF has been uploaded yet!")

# -----------------------------------------------------------------------
# 3. ENDPOINTS
# -----------------------------------------------------------------------

# --- NEW UPLOAD ENDPOINT ---
@app.post("/upload-pdf")
async def upload_pdf_endpoint(file: UploadFile = File(...)):
    temp_file_path = f"temp_{file.filename}"
    
    try:
        # Step A: Save the incoming frontend file temporarily to your disk
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        # Step B: Pass the temporary file to your PDF teammate's code
        print(f"📄 Processing PDF: {file.filename}...")
        raw_chunks = process_pdf(temp_file_path)
        
        if not raw_chunks:
            os.remove(temp_file_path)
            return {"status": "error", "message": "No text could be extracted from this PDF."}
        
        # --- THE FIX: Translate raw strings into the dictionaries RAG expects ---
        extracted_chunks = []
        for i, chunk_data in enumerate(raw_chunks):
            if isinstance(chunk_data, str):
                # Wrap the raw string in the dictionary RAG wants
                extracted_chunks.append({
                    "chunk_id": i + 1,
                    "text": chunk_data,
                    "page": 1 # Default page number since it's missing
                })
            else:
                # If it's already a dictionary, leave it alone
                extracted_chunks.append(chunk_data)
        
        # Step C: Pass those beautifully formatted chunks to your RAG partner's index builder
        print("🧠 Building AI Search Index...")
        rag.build_index(extracted_chunks)
        
        # Step D: Save it so the server remembers it for the chat endpoint
        rag.save(RAG_INDEX_PATH)
        
        # Clean up the temporary file
        os.remove(temp_file_path)
        
        return {"status": "success", "message": f"{file.filename} processed and indexed successfully!"}
        
    except Exception as e:
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
        return {"status": "error", "message": f"Failed to process file: {str(e)}"}

# --- CHAT ENDPOINT ---
class ChatRequest(BaseModel):
    user_id: str
    message: str

class ChatResponse(BaseModel):
    status: str
    bot_response: str

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    incoming_text = request.message
    
    try:
        matched_chunks = rag.retrieve(incoming_text, k=2)
        
        if not matched_chunks:
            bot_answer = "I searched the documents but couldn't find any information relevant to your question."
        else:
            bot_answer = "\n\n".join([f"[From Page {c.get('page', '?')}]: {c.get('text', '')}" for c in matched_chunks])
            
    except Exception as e:
        bot_answer = f"The RAG engine encountered an issue processing your request: {str(e)}"
        
    return ChatResponse(
        status="success",
        bot_response=bot_answer
    )