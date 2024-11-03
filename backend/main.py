from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import services.chat as ChatService

app = FastAPI()

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Data model for the chatbot request
class ChatRequest(BaseModel):
    message: str

# Handle chat requests and communicate with the Hugging Face model
@app.post("/chat")
async def chat(request: ChatRequest):
    response = ChatService.redirect_user_query(request.message)
    return response
