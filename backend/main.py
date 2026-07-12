from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="Academic Tutor API")

# This tells the server to allow requests from other websites
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # The "*" means "allow any website" for now
    allow_credentials=True,
    allow_methods=["*"],  # Allows all types of requests (POST, GET, etc.)
    allow_headers=["*"],
)

# ---------------------------------------------------------
# 1. THE DATA RULES (Contracts)
# ---------------------------------------------------------
# This forces the Frontend to send a user_id and a message
class ChatRequest(BaseModel):
    user_id: str
    message: str

# This forces your server to reply with a status and a response
class ChatResponse(BaseModel):
    status: str
    bot_response: str

# ---------------------------------------------------------
# 2. THE DUMMY AI (Your temporary placeholder)
# ---------------------------------------------------------
# You will delete this function later when the AI team is done.
def get_fake_ai_answer(user_message: str) -> str:
    print(f"Backend received the message: {user_message}")
    
    # We return a fake string just to prove the server works
    return f"This is a fake AI answer. You asked: {user_message}"

# ---------------------------------------------------------
# 3. THE SERVER ENDPOINT (The Waiter)
# ---------------------------------------------------------
@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    
    # 1. Read what the frontend sent
    incoming_text = request.message
    
    # 2. Send it to our dummy function (for now)
    # LATER: You will change this to the AI team's real function
    answer = get_fake_ai_answer(incoming_text)
    
    # 3. Package it up and send it back to the frontend
    return ChatResponse(
        status="success",
        bot_response=answer
    )