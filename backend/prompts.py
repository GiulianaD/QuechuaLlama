redirection_prompt = """
    I will give you a USER QUERY. Your task is to analyze the query and classify it based on the following criteria, returning ONLY the corresponding number:

    1. The query is a request for translation from Spanish to Quechua.
    2. The query is related to Guarani, Quechua, or Aymara deities. This includes questions related to:
        - Querying the names of all defined deities.
        - Retrieving symbolic meanings (simbolismo) associated with each deity.
        - Finding out which festivities (festividad) are related to specific deities.
        - Identifying the culture (cultura) connected to each deity.
        - Listing all festivities by their name.
        - Retrieving information on cultures by name.
        - Discovering which festivities are tied to a particular culture.
        - Identifying which culture is associated with specific festivities via deities related to both.
        - Generating a comprehensive list of deities with their connected cultures and festivities.

        if it is not any of these, then it doesn't classify as 2.
    3. The query does not meet either of the above criteria.
    
    Example Input:
    USER QUERY: "Translate this text from Spanish to Quechua: 'La biblia dice que Jehová es bueno'"

    Expected Output (only the number):
    1

    Now, please classify the following USER QUERY: "
"""

sparql_prompt = """
    I have defined an ontology in RDF as shown below:

    @prefix ns1: <http://example.org/mythology/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

    ns1:cultura a rdfs:Class ;
        rdfs:label "cultura"^^xsd:string .

    ns1:deidad a rdfs:Class ;
        rdfs:label "deidad"^^xsd:string .

    ns1:festividad a rdfs:Class ;
        rdfs:label "festividad"^^xsd:string .

    ns1:cultura_id a rdf:Property ;
        rdfs:label "id"^^xsd:string ;
        rdfs:domain ns1:cultura ;
        rdfs:range "integer"^^xsd:string .

    ns1:cultura_nombre a rdf:Property ;
        rdfs:label "nombre"^^xsd:string ;
        rdfs:domain ns1:cultura ;
        rdfs:range "character varying"^^xsd:string .

    ns1:deidad_cultura a rdf:Property ;
        rdfs:label "cultura"^^xsd:string ;
        rdfs:domain ns1:deidad ;
        rdfs:range "integer"^^xsd:string .

    ns1:deidad_festividad a rdf:Property ;
        rdfs:label "festividad"^^xsd:string ;
        rdfs:domain ns1:deidad ;
        rdfs:range "integer"^^xsd:string .

    ns1:deidad_id a rdf:Property ;
        rdfs:label "id"^^xsd:string ;
        rdfs:domain ns1:deidad ;
        rdfs:range "integer"^^xsd:string .

    ns1:deidad_nombre a rdf:Property ;
        rdfs:label "nombre"^^xsd:string ;
        rdfs:domain ns1:deidad ;
        rdfs:range "character varying"^^xsd:string .

    ns1:deidad_simbolismo a rdf:Property ;
        rdfs:label "simbolismo"^^xsd:string ;
        rdfs:domain ns1:deidad ;
        rdfs:range "text"^^xsd:string .

    ns1:festividad_id a rdf:Property ;
        rdfs:label "id"^^xsd:string ;
        rdfs:domain ns1:festividad ;
        rdfs:range "integer"^^xsd:string .

    ns1:festividad_nombre a rdf:Property ;
        rdfs:label "nombre"^^xsd:string ;
        rdfs:domain ns1:festividad ;
        rdfs:range "character varying"^^xsd:string .

    ns1:has_festividad a rdf:Property ;
        rdfs:label "has festividad"^^xsd:string ;
        rdfs:domain ns1:deidad ;
        rdfs:range ns1:festividad .

    ns1:has_cultura a rdf:Property ;
        rdfs:label "has cultura"^^xsd:string ;
        rdfs:domain ns1:deidad ;
        rdfs:range ns1:cultura .

    Task: I will provide you with a query in natural language. Your goal is to translate it to a SPARQL query
     following the previous ontology specifications (properties' names and classes' names).

    Output Format:
    Return only the SPARQL query (don't include any other text)

    Here is the USER QUERY:
"""