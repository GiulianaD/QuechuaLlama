from SPARQLWrapper import SPARQLWrapper, JSON

sparql = SPARQLWrapper("http://WindowsGD:7200/repositories/Mythology")

sparql.setQuery("""
PREFIX mith: <http://example.org/mythology/>

SELECT  ?festividad (COUNT(?diosName) AS ?numDios)
WHERE {
    ?dios a mith:deidad;
    	mith:deidad_nombre ?diosName;
    	mith:has_festividad ?festividad.
    ?festividad a mith:festividad.
}

GROUP BY ?festividad
HAVING (?numDios > 1)
""")
sparql.setReturnFormat(JSON)

results = sparql.query().convert()
print(results)