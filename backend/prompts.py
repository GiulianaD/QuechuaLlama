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