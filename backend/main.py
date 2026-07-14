import sys
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# -----------------------------------------------------------------------
# 1. PYTHON PATH RESOLUTION (So backend can see the RAG folder)
# -----------------------------------------------------------------------
# Find where main.py is, go up one level to the root project folder, and add it to Python's memory
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(CURRENT_DIR)
sys.path.append(ROOT_DIR)

# Import your partner's RAGIndex class from RAG/rag_module.py
from RAG.rag_module import RAGIndex

app = FastAPI(title="Academic Tutor API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------------------------------------------------
# 2. INITIALIZE THE RAG ENGINE ON STARTUP
# -----------------------------------------------------------------------
# Point directly to where the 'saved_index' folder lives inside the RAG directory
RAG_INDEX_PATH = os.path.join(ROOT_DIR, "RAG", "saved_index")

rag = RAGIndex()

try:
    # Load the database once when the server starts up so it stays fast
    rag.load(RAG_INDEX_PATH)
    print("🚀 SUCCESS: RAG Index loaded perfectly into Backend!")
except Exception as e:
    print(f"⚠️ WARNING: Could not load RAG index: {e}")
    print("Make sure your partner ran 'python RAG/rag_module.py' first to generate the index data!")

# -----------------------------------------------------------------------
# 3. DATA CONTRACTS & ENDPOINTS
# -----------------------------------------------------------------------
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
        # Ask her RAG engine to find the top 2 closest paragraphs from the PDF
        matched_chunks = rag.retrieve(incoming_text, k=2)
        
        if not matched_chunks:
            bot_answer = "I searched the documents but couldn't find any information relevant to your question."
        else:
            # Stitched text chunks serve as a highly functional placeholder 
            # until the AI Features teammate provides the clean LLM text wrapper
            bot_answer = "\n\n".join([f"[From Page {c['page']}]: {c['text']}" for c in matched_chunks])
            
    except Exception as e:
        bot_answer = f"The RAG engine encountered an issue processing your request: {str(e)}"
        
    return ChatResponse(
        status="success",
        bot_response=bot_answer
    )