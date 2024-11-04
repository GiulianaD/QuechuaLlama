from prompts import redirection_prompt, quechua_translation_prompt 
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

#extraction of the translated text
def extract_translation(response):
    start_phrase = "Respond only with the Quechua translation, without any additional text."
    if start_phrase in response:
        translation = response.split(start_phrase)[-1].strip()
        return translation
    return response

# Translates a Spanish query to Quechua using the LLM.
def translate_spanish_to_quechua(query: str) -> dict:
    prompt = quechua_translation_prompt.format(query=query)
    translation_response = llama_quechua_client.get_response(prompt)
    translation = extract_translation(translation_response)
    return {"response": translation}

# Generates a default response for unsupported queries.
def generate_default_response() -> dict:
    return {"response": "I am sorry. I am not trained to answer that question."}

# Generates an error response with a custom message.
def generate_error_response(message: str) -> dict:
    return {"response": message}
