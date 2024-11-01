# main.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import os
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env
load_dotenv()

app = FastAPI()

# Obtener el token desde la variable de entorno
HUGGING_FACE_API_TOKEN = os.getenv("HUGGING_FACE_API_TOKEN")
API_URL = "https://api-inference.huggingface.co/models/meta-llama/Llama-3.2-3B"

# Verifica que el token esté configurado
if not HUGGING_FACE_API_TOKEN:
    raise ValueError("El token de Hugging Face no está configurado. Verifica el archivo .env.")

headers = {
    "Authorization": f"Bearer {HUGGING_FACE_API_TOKEN}"
}

# Modelo de datos para la solicitud del chatbot
class ChatRequest(BaseModel):
    message: str

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
