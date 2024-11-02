from fastapi import HTTPException
import requests
import os
from dotenv import load_dotenv
from prompts import redirection_prompt
from huggingface_hub import InferenceClient

load_dotenv()

HUGGING_FACE_API_TOKEN = os.getenv("HUGGING_FACE_API_TOKEN")
API_URL = "https://api-inference.huggingface.co/models/meta-llama/Llama-3.2-3B-Instruct"
client = InferenceClient(api_key=HUGGING_FACE_API_TOKEN)

if not HUGGING_FACE_API_TOKEN:
    raise ValueError("The Hugging Face token is not configured. Check the .env file.")

headers = {
    "Authorization": f"Bearer {HUGGING_FACE_API_TOKEN}",
    "Content-Type": "application/json"
}

def redirectUserQuery(query):
    prompt = redirection_prompt + query + "\""

    messages = [
        { "role": "user", "content": prompt }
    ]

    stream = client.chat.completions.create(
        model="meta-llama/Llama-3.2-3B-Instruct", 
        messages=messages, 
        max_tokens=500,
        stream=True
    )

    response = ""
    for chunk in stream:
        response += chunk.choices[0].delta.content

    try:
        if (int(response) == 1):
            return {"response": "This is a translation task"}
        elif (int(response) == 2):
            return {"response": "This is a question about deities"}
        else:
            return {"response": "I am sorry. I am not trained to answer that question."}
    except ValueError:
        print("The LLM didn't return the appropriate response.")
        
def queryKnowledgeGraph(query):
    pass

def translateSpanish2Quechua(query):
    pass