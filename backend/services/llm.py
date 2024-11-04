from fastapi import HTTPException
from dotenv import load_dotenv
from huggingface_hub import InferenceClient
from services.config import LLAMA_QUECHUA_API_URL
import requests
import os

load_dotenv()

HUGGING_FACE_API_TOKEN = os.getenv("HUGGING_FACE_API_TOKEN")

if not HUGGING_FACE_API_TOKEN:
    raise ValueError("The Hugging Face API token is missing. Please configure it in the .env file.")


class ModelClientFactory:
    @staticmethod
    def create_client(model_type: str):
        if model_type == "LLAMA":
            return LlamaModelClient()
        elif model_type == "QUECHUA":
            return QuechuaModelClient()
        else:
            raise ValueError(f"Unknown model type: {model_type}")

class LlamaModelClient:
    def __init__(self):
        self.client = InferenceClient(api_key=HUGGING_FACE_API_TOKEN)
        self.model = "meta-llama/Llama-3.2-3B-Instruct"
        self.max_tokens = 500

    def get_response(self, prompt: str) -> str:
        messages = [{"role": "user", "content": prompt}]
        response_text = ""
        try:
            stream = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=self.max_tokens,
                stream=True
            )
            for chunk in stream:
                response_text += chunk.choices[0].delta.content
        except Exception as e:
            print(f"Error generating text from Llama model: {e}")
            raise HTTPException(status_code=500, detail="Error generating text from Llama model.")
        return response_text

class QuechuaModelClient:
    def __init__(self):
        self.url = LLAMA_QUECHUA_API_URL
        self.headers = {
            "Authorization": f"Bearer {HUGGING_FACE_API_TOKEN}",
            "Content-Type": "application/json"
        }

    def get_response(self, prompt: str) -> str:
        payload = {"inputs": prompt}
        try:
            response = requests.post(self.url, headers=self.headers, json=payload)
            if response.status_code != 200:
                raise HTTPException(status_code=response.status_code, detail="Error connecting to the Hugging Face model.")
            response_data = response.json()
            generated_text = response_data[0].get("generated_text") if isinstance(response_data, list) else response_data.get("generated_text")
            if not generated_text:
                raise ValueError("The model response did not contain generated text.")
        except requests.RequestException as e:
            print(f"Error requesting response from Quechua model: {e}")
            raise HTTPException(status_code=500, detail="Error connecting to the Quechua model.")
        return generated_text

llama_client = ModelClientFactory.create_client("LLAMA")
llama_quechua_client = ModelClientFactory.create_client("QUECHUA")