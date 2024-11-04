redirection_prompt = """
    I will give you a USER QUERY. Your task is to analyze the query and classify it based on the following criteria, returning ONLY the corresponding number:

    1. The query is a request for translation from Spanish to Quechua.
    2. The query is related to Guaraní, Quechua, or Aymara deities. This includes questions related to:
        - Finding out what deities has each culture.
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
rdf_schema = """
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

"""
sparql_prompt = f"""
    I have defined an ontology in RDF as shown below:

    ** RDF SCHEMA **
    {rdf_schema}

    ** TASK **
     
    I will provide you with a query in natural language. Your goal is to translate it to a SPARQL query
     following the previous ontology specifications (properties' names and classes' names).

    ** EXAMPLE 1**

    USER QUERY: 'Qué festividad tiene el dios inti?'
    EXPECTED OUTPUT: 
        "
        PREFIX ns1: <http://example.org/mythology/>
        SELECT ?festividadNombre ?deidadNombre
        WHERE {{
            ?deidad ns1:has_festividad ?festividad;
                    ns1:deidad_nombre ?deidadNombre.
            ?festividad a ns1:festividad;
                ns1:festividad_nombre ?festividadNombre.
            FILTER(?deidadNombre = "Inti")
        }}
        " 
    ** EXAMPLE 2**

    USER QUERY: 'Qué dioses de la cultura guaraní y de la cultura quechua existen?'
    EXPECTED OUTPUT:
    "
        PREFIX ns1: <http://example.org/mythology/>
        SELECT ?deidadNombre
        WHERE {{
            ?cultura a ns1:cultura;
                ns1:cultura_nombre ?culturaNombre.
            ?deidad a ns1:deidad;
                    ns1:has_cultura ?cultura;
                    ns1:deidad_nombre ?deidadNombre.
            FILTER (?culturaNombre = "Aymara" || ?culturaNombre = "Quechua")
        }}
    "

    **EXAMPLE 3**
    USER QUERY: Qué simboliza el dios Mamani de la cultura aymara?
    EXPECTED OUTPUT:
    "
    PREFIX ns1: <http://example.org/mythology/>
    SELECT ?simbolismo
    WHERE {{
        ?cultura a ns1:cultura;
            ns1:cultura_nombre ?culturaNombre.
        ?deidad a ns1:deidad;
                ns1:has_cultura ?cultura;
                ns1:deidad_nombre ?deidadNombre;
                ns1:deidad_simbolismo ?simbolismo;
        
        FILTER (?culturaNombre = "Aymara" && ?deidadNombre = "Mamani")
    }}
    "
    ** OUTPUT FORMAT REMINDER **

    Return only a valid SPARQL query (don't include any other text, nor special characters, the variables in the format ?variable must be well written) and the results 
    should only return what is asked in the question.

    ** INPUT **
"""

verbalize_triplet_prompt = """
    ** TASK **
    You will receive a user query and a triplet as the result of a SPARQL query. Your task is to verbalize the information in the triplet to answer the user query in clear, simple language. Ensure that the response is easy to understand, concise, and relevant to the user query.

    ** GUIDELINES **

    Interpret the triplet in relation to the user query.
    Use plain language, avoiding technical jargon.
    Ensure your response directly addresses the user's question.
    
    ** TRIPLET **
"""

quechua_translation_prompt = """
    Please translate the following text from Spanish to Quechua: '{query}'. 
    Respond only with the Quechua translation, without any additional text.
"""