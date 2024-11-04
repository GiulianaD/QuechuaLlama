from SPARQLWrapper import SPARQLWrapper, JSON
from services.config import GRAPH_DB_URL
from prompts import sparql_prompt, verbalize_triplet_prompt
from services.llm import llama_client

sparql_client = SPARQLWrapper(GRAPH_DB_URL)

# Generates a SPARQL query string based on user input.
def generate_sparql_query(query: str) -> str:
    prompt = f"{sparql_prompt}{query}\""
    sparql_query = llama_client.get_response(prompt)
    return sparql_query.replace('\n', ' ')

# Executes a SPARQL query against the knowledge graph and returns a human-readable response.
def query_knowledge_graph(query: str) -> dict:
    sparql_query = generate_sparql_query(query)
    
    try:
        sparql_client.setQuery(sparql_query)
        sparql_client.setReturnFormat(JSON)
        results = sparql_client.query().convert()
        verbalized_response = verbalize_sparql_results(query, results)
        return {"response": verbalized_response}
    except Exception as e:
        print(f"Error querying knowledge graph: {e}")
        return generate_error_response("Malformed SPARQL query.")

# Converts SPARQL query results into a human-readable format.
def verbalize_sparql_results(query: str, results) -> str:
    prompt = f"{verbalize_triplet_prompt}{str(results)}\"\n ** ORIGINAL QUERY **\n\"{query}\""
    return llama_client.get_response(prompt)

# Generates a standard error response for SPARQL query failures.
def generate_error_response(message: str) -> dict:
    return {"response": message}
