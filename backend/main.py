from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI()

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Set the Hugging Face API token and the API URL for the Llama model
HUGGING_FACE_API_TOKEN = os.getenv("HUGGING_FACE_API_TOKEN")
API_URL = "https://api-inference.huggingface.co/models/meta-llama/Llama-3.2-3B"

# Check that the token is configured
if not HUGGING_FACE_API_TOKEN:
    raise ValueError("The Hugging Face token is not configured. Please check the .env file.")

headers = {
    "Authorization": f"Bearer {HUGGING_FACE_API_TOKEN}"
}

# Data model for the chatbot request
class ChatRequest(BaseModel):
    message: str

# Handle chat requests and communicate with the Hugging Face model
@app.post("/chat")
async def chat(request: ChatRequest):
    payload = {
        "inputs": request.message
    }

    response = requests.post(API_URL, headers=headers, json=payload)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Error al conectarse al modelo de Hugging Face")

    response_data = response.json()
    generated_text = response_data[0].get("generated_text") if isinstance(response_data, list) else response_data.get("generated_text")
    
    return {"response": generated_text}
