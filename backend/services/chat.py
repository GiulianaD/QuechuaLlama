from prompts import redirection_prompt
from services.llm import llama_client, llama_quechua_client
from services.graphdb import query_knowledge_graph

# Directs the user's query to the correct handler based on the LLM response code.
def handle_user_query(query: str) -> dict:
    prompt = f"{redirection_prompt}{query}\""
    response = llama_client.get_response(prompt)

    try:
        response_code = int(response)
        if response_code == 1:
            return translate_spanish_to_quechua(query)
        elif response_code == 2:
            return query_knowledge_graph(query)
        else:
            return generate_default_response()
    except ValueError:
        print("Warning: The LLM returned an invalid response code.")
        return generate_error_response("Invalid response from model.")

# Translates a Spanish query to Quechua using the LLM.
def translate_spanish_to_quechua(query: str) -> dict:
    translation = llama_quechua_client.get_response(query)
    return {"response": translation}

# Generates a default response for unsupported queries.
def generate_default_response() -> dict:
    return {"response": "I am sorry. I am not trained to answer that question."}

# Generates an error response with a custom message.
def generate_error_response(message: str) -> dict:
    return {"response": message}
