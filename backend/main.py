from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import os
from dotenv import load_dotenv
import services.chat as ChatService

# Cargar variables de entorno desde el archivo .env
load_dotenv()

app = FastAPI()

# Obtener el token desde la variable de entorno
HUGGING_FACE_API_TOKEN = os.getenv("HUGGING_FACE_API_TOKEN")
API_URL = "https://api-inference.huggingface.co/models/meta-llama/Llama-3.2-3B-Instruct"

# Verifica que el token esté configurado
if not HUGGING_FACE_API_TOKEN:
    raise ValueError("The Hugging Face token is not configured. Check the .env file.")

headers = {
    "Authorization": f"Bearer {HUGGING_FACE_API_TOKEN}",
    "Content-Type": "application/json"
}

# Modelo de datos para la solicitud del chatbot
class ChatRequest(BaseModel):
    message: str


@app.post("/chat")
async def chat(request: ChatRequest):
    response = ChatService.redirectUserQuery(request.message)
    return response
