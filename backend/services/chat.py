from fastapi import HTTPException
import requests
import os
from dotenv import load_dotenv
from prompts import redirection_prompt, sparql_prompt, verbalize_triplet_prompt
from huggingface_hub import InferenceClient
from SPARQLWrapper import SPARQLWrapper, JSON

load_dotenv()

HUGGING_FACE_API_TOKEN = os.getenv("HUGGING_FACE_API_TOKEN")
API_URL = "https://api-inference.huggingface.co/models/meta-llama/Llama-3.2-3B-Instruct"
API_URL_QU = "https://api-inference.huggingface.co/models/giulianad/LlamaQuechuaFT_1ep_1e-4LR"

client = InferenceClient(api_key=HUGGING_FACE_API_TOKEN)
sparql = SPARQLWrapper("http://SELWA:7200/repositories/Mythology3")

# Check that the token is configured
if not HUGGING_FACE_API_TOKEN:
    raise ValueError("The Hugging Face token is not configured. Please check the .env file.")

headers = {
    "Authorization": f"Bearer {HUGGING_FACE_API_TOKEN}",
    "Content-Type": "application/json"
}

LLAMA_MODEL = "meta-llama/Llama-3.2-3B-Instruct"
MAX_TOKENS = 500

# OPTION 1 - Optimized for meta-llama/Llama-3.2-3B-Instruct
def create_chat_completion(prompt: str) -> str:
    messages = [{"role": "user", "content": prompt}]
    
    stream = client.chat.completions.create(
        model=LLAMA_MODEL, 
        messages=messages, 
        max_tokens=MAX_TOKENS,
        stream=True
    )

    response = ""
    for chunk in stream:
        response += chunk.choices[0].delta.content
    return response

# OPTION 2 - Better for the fine-tuned model
def get_response_from_llm(prompt):
    payload = {
    "inputs": prompt
    }
    response = requests.post(API_URL_QU, headers=headers, json=payload)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Error al conectarse al modelo de Hugging Face")

    response_data = response.json()
    generated_text = response_data[0].get("generated_text") if isinstance(response_data, list) else response_data.get("generated_text")
    
    return generated_text

# Redirects the user's query to the appropriate handler
def redirect_user_query(query: str) -> dict:
    prompt = f"{redirection_prompt}{query}\""
    response = create_chat_completion(prompt)
    #response = get_response_from_llm(prompt)
    try:
        response_code = int(response)
        if response_code == 1:
            return translateSpanish2Quechua(query)
        elif response_code == 2:
            return query_knowledge_graph(query)
        else:
            return {"response": "I am sorry. I am not trained to answer that question."}
    except ValueError:
        print("The LLM didn't return an appropriate response.")
        return {"response": "Invalid response from model."}

# Generates a SPARQL query based on the provided input.
def get_sparql_query(query: str) -> str:
    prompt = f"{sparql_prompt}{query}\""
    sparql_response = create_chat_completion(prompt)
    return sparql_response.replace('\n', ' ')

#Queries the knowledge graph using a SPARQL query.
def query_knowledge_graph(query: str) -> dict:
    sparql_query = get_sparql_query(query)
    try:
        sparql.setQuery(sparql_query)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        verbalized_response = verbalize_sparql_results(query, results)
        return {"response": verbalized_response}
    except Exception as e:
        print(f"Error querying knowledge graph: {e}")
        return {"response": "MALFORMED SPARQL QUERY"}

# Verbalizes the SPARQL results into a human-readable format
def verbalize_sparql_results(query: str, results) -> str:
    prompt = f"{verbalize_triplet_prompt}{str(results)}\"\n ** ORIGINAL QUERY**\n\"{query}\""
    return create_chat_completion(prompt)

def translateSpanish2Quechua(query):
    prompt = query
    translation = get_response_from_llm(prompt)
    return {"response": translation}