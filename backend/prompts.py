redirection_prompt = """
    I will give you a USER QUERY. Your task is to analyze the query and classify it based on the following criteria, returning ONLY the corresponding number:

    1. The query is a request for translation from Spanish to Quechua.
    2. The query is related to Guarani, Quechua, or Aymara deities. This includes questions related to:
        - Culture name.
        - Names of deities or symbolic meaning,
        - Festivities or rituals connected to these deities.
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
    Task: I will provide you with a query in natural language. Your goal is to determine whether this query can be translated into SPARQL using only the properties and classes defined in the ontology above. If it can, translate it to SPARQL.

    Output Format:
    Return the result in JSON format with the following keys:

    "canBeTranslated": Indicate if the query can be translated, with 1 for "yes" and 0 for "no."
    "SPARQL": Provide the translated SPARQL query if possible; otherwise, return an empty string.
    Output Example: If the translation is possible:

    json
    Copy code
    {
        "canBeTranslated": 1,
        "SPARQL": "[the generated SPARQL query]"
    }
    If the translation is not possible:

    json
    Copy code
    {
        "canBeTranslated": 0,
        "SPARQL": ""
    }
    Here is the USER QUERY:
"""